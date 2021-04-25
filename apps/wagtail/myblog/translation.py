
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from .models import BlogIndexPage, BlogPage

@register(BlogPage)
class BlogPageTr(TranslationOptions):
    fields = ('body',)

@register(BlogIndexPage)
class BlogIndexPageTr(TranslationOptions):
    fields = ()