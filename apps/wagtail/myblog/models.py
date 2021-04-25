from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from apps.wagtail.streams import blocks
from apps.wagtail.home.models import MyPage
from .blocks import BodyBlock
from taggit.models import Tag

from blog.abstract import (
    BlogCategoryAbstract,
    BlogCategoryBlogPageAbstract,
    BlogIndexPageAbstract,
    BlogPageAbstract,
    BlogPageTagAbstract
)


COMMENTS_APP = getattr(settings, 'COMMENTS_APP', None)


class BlogIndexPage(BlogIndexPageAbstract, MyPage):
    class Meta:
        verbose_name = _('Blog index')

    @property
    def blogs(self):
        # Get list of blog pages that are descendants of this page
        blogs = BlogPage.objects.descendant_of(self).live()
        blogs = blogs.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return blogs

    def get_context(self, request, tag=None, category=None, author=None, *args,
                    **kwargs):
        context = super(BlogIndexPage, self).get_context(
            request, *args, **kwargs)
        blogs = self.blogs

        categories = BlogCategory.objects.all()
        context['categories'] = categories

        tags = BlogTag.objects.all()
        context['tags'] = tags  

        if tag is None:
            tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    BlogCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(BlogCategory, slug=category)
            blogs = blogs.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                blogs = blogs.filter(author__username=author)
            else:
                blogs = blogs.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        if hasattr(settings, 'BLOG_PAGINATION_PER_PAGE'):
            page_size = settings.BLOG_PAGINATION_PER_PAGE

        paginator = None
        if page_size is not None:
            paginator = Paginator(blogs, page_size)  # Show 10 blogs per page
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)

        context['blogs'] = blogs
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context['COMMENTS_APP'] = COMMENTS_APP
        context['paginator'] = paginator
        context = get_blog_context(context)

        return context

    subpage_types = ['myblog.BlogPage']


@register_snippet
class BlogCategory(BlogCategoryAbstract):
    class Meta:
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")


class BlogCategoryBlogPage(BlogCategoryBlogPageAbstract):
    class Meta:
        pass


class BlogPageTag(BlogPageTagAbstract):
    class Meta:
        pass


@register_snippet
class BlogTag(Tag):
    class Meta:
        proxy = True


def get_blog_context(context):
    """ Get context data useful on all blog related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='blogpage'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = BlogCategory.objects.all()
    context['root_categories'] = BlogCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        blog_count=Count('blogpage'),
    )
    return context


class BlogPage(BlogPageAbstract, MyPage):

    body = StreamField(BodyBlock(), blank=True)

    class Meta:
        verbose_name = _('Blog page')
        verbose_name_plural = _('Blog pages')

    def get_blog_index(self):
        # Find closest ancestor which is a blog index
        return self.get_ancestors().type(BlogIndexPage).last()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blogs'] = self.get_blog_index().blogindexpage.blogs


        categories = self.blog_categories.all()
        context['categories'] = categories 
        print('cat', categories)
        tags = self.tags.all()
        context['tags'] = tags  
        context = get_blog_context(context)
        context['COMMENTS_APP'] = COMMENTS_APP
        return context

    parent_page_types = ['myblog.BlogIndexPage']
    content_panels = [
        FieldPanel('title', classname="full title"),
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('blog_categories'),
        ], heading="Tags and Categories"),
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
    ]