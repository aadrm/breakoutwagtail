from .models import (
    HomePage,
    RoomPage,
    BooknowPage,
    CookieSettingsPage,
)
from blog.models import BlogIndexPage, BlogPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'our_rooms_header',
        'our_rooms_text',
        'faq',
    )

@register(RoomPage)
class HomePageTR(TranslationOptions):
    fields = (
    )

@register(BooknowPage)
class BooknowPageTR(TranslationOptions):
    fields = (
    )

@register(CookieSettingsPage)
class CookieSettingsPageTR(TranslationOptions):
    fields = (
    )
# django cookie consent
from cookie_consent.models import CookieGroup, Cookie

@register(CookieGroup)
class CookieGroupTR(TranslationOptions):
    fields = (
        'name',
        'description',
    )

@register(Cookie)
class CookieTR(TranslationOptions):
    fields = (
        'description',
    )



@register(BlogPage)
class BlogPageTr(TranslationOptions):
    fields = (
        'body',
    )

@register(BlogIndexPage)
class BlogIndexPageTr(TranslationOptions):
    fields = ()