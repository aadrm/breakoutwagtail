from .models import (
    MyPage,
    HomePage,
    RoomPage,
    BooknowPage,
    CouponsPage,
    CookieSettingsPage,
)
from blog.models import BlogIndexPage, BlogPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register
from wagtail.core.models import Page

class PageTr(TranslationOptions):
    fields = (
        'title',
    )


@register(MyPage)
class MyPageTR(TranslationOptions):
    fields = (
        'header_image_alt',
        'seo_image_alt',
    )


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'reviews',
        'group_offers',
        'our_rooms_header',
        'our_rooms_text',
        'online_header',
        'online_text',
        'video_header',
        'video_text',
        'offers_header',
        'offers_text',
        'prices_header',
        'prices_text',
        'reviews_header',
        'reviews_text',
        'faq',
    )

@register(RoomPage)
class HomePageTR(TranslationOptions):
    fields = (
    )

@register(CouponsPage)
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