# django cookie consent
from blog.models import BlogIndexPage, BlogPage, 
from cookie_consent.models import CookieGroup, Cookie
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from wagtail.core.model import Page



@register(BlogPage)
class BlogPageTr(TranslationOptions):
    fields = (
        'body'
    )

@register(BlogIndexPage)
class BlogIndexPageTr(TranslationOptions):
    fields = ()
    
@register(CookieGroup)
class CookieGroupTR(TranslationOptions):
    fields = (
        'name',
        'description',
    )