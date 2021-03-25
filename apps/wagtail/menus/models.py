"""menus/models.py"""
from django.db import models

from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


class Document(Orderable):

    name = models.CharField(max_length=48)
    icon = models.TextField()
    document = models.ForeignKey("wagtaildocs.Document", on_delete=models.CASCADE)
    docs = ParentalKey("DocumentCollection", related_name="documents")

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('document'),
    ]

        

@register_snippet
class DocumentCollection(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    # slug = models.SlugField()

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("documents", label="Document")
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):

    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )

    uri_fragment = models.CharField(max_length=50, null=True, blank=True)

    sub_menu = models.ForeignKey(
        "menus.Menu",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    fixed = models.BooleanField(default=False, blank=True)

    noopener = models.BooleanField(default=False, blank=True)

    new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("uri_fragment"),
        PageChooserPanel("link_page"),
        FieldPanel("fixed"),
        FieldPanel("new_tab"),
        FieldPanel("noopener"),
        SnippetChooserPanel("sub_menu"),
    ]


    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        else:
            return ''

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'

    def save(self, *args, **kwargs):
        menus = [self.sub_menu]
        if self.sub_menu == self.page:
            print('error')
            return
        super(MenuItem,self).save(*args, **kwargs)

        

@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    # slug = models.SlugField()

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
