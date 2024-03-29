from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, translate_url
from django.shortcuts import render
from django.utils import translation
from django.conf import settings

from wagtail.core import blocks
from wagtail.core import fields
from wagtail.utils.decorators import cached_classmethod
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel, ImageFieldComparison
from wagtail.core.fields import StreamField, StreamBlock, BlockField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from apps.booking.models import Room

from django.utils.translation import ugettext_lazy as _

from apps.wagtail.menus.models import WagtailLanguage
from apps.booking.models import Room, ProductFamily
from apps.booking.forms import AddProductToCartForm 
from apps.booking.utils import get_cart
from apps.wagtail.streams import blocks as myblocks

class MyPage(Page):

    Page.search_description.max_length = 100
    header_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Header Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
    )
    header_image_alt = models.CharField(max_length=128, null=True, blank=True)
    seo_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Seo Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
    )
    seo_image_alt = models.CharField(max_length=128, null=True, blank=True)
    noindex = models.BooleanField(default=False)
    extra_schema = models.TextField(max_length=128, null=True, blank=True)
    keywords = models.CharField('Keywords', max_length=100, blank=True, null=True)
    translations = ParentalManyToManyField(WagtailLanguage, blank=True)

    def get_context(self, request):
        print('lang', WagtailLanguage.objects.all())
        translations = list(self.translations.all())
        try:
            default_lang = WagtailLanguage.objects.get(language_code=settings.LANGUAGES[0][0])
        except Exception:
            default_lang = None
        try:
            current_lang = WagtailLanguage.objects.get(language_code=translation.get_language())
            translations.remove(current_lang)
            translations.insert(0, current_lang)
        except Exception:
            current_lang = None
        alternatives = list(translations)


        # figure out if the current language is translated
        if current_lang in translations:
            canonical = current_lang 
        else:
            canonical = default_lang

        context = super().get_context(request)
        context['language_canonical'] = canonical
        context['language_all'] = translations 
        context['language_alternatives'] = alternatives
        return context

    def get_sitemap_urls(self, request):
        if self.noindex:
            return []
        else:
            default_lang = settings.LANGUAGE_CODE
            translation.activate(default_lang)



            sitemap =  super().get_sitemap_urls(request)
            return sitemap

    class Meta:
        abstract = True

    content_panels = Page.content_panels + [
        MultiFieldPanel (
            heading="Header Image",
            children = [
                ImageChooserPanel("header_image"),
                FieldPanel("header_image_alt")
            ]
        )
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel (
            heading="Seo Image",
            children = [
                ImageChooserPanel("seo_image"),
                FieldPanel("seo_image_alt")
            ]
        ),
        FieldPanel('noindex'),
        FieldPanel('translations'),
        FieldPanel('extra_schema'),
    ]

    @cached_classmethod
    def get_edit_handler(cls):
        edit_handler = TabbedInterface([
            ObjectList(cls.content_panels, heading=('Content')),
            ObjectList(cls.promote_panels, heading=('Promotion')),
            ObjectList(cls.settings_panels, heading=('Settings')),
            YoastPanel(
                keywords='keywords',
                title='seo_title',
                search_description='search_description',
                slug='slug'
            ),
        ])
        return edit_handler.bind_to(model=cls)

class LinkPage(MyPage):

    class Meta:
        abstract = True
    
    content_panels = [FieldPanel('title')]
    promote_panels = [
        FieldPanel('slug')

    ]

class BooknowPage(RoutablePageMixin, MyPage):

    max_count = 1
    template = "home/book_page.html"


    content = StreamField(
        [
            ('section', myblocks.SectionBlock()),
        ],
        null=True,
        blank=True,
    )

    content_after = StreamField(

        [
            ('section', myblocks.SectionBlock()),
        ],
        null=True,
        blank=True,
    )

 
    content_panels = MyPage.content_panels + [
        StreamFieldPanel('content'),
        StreamFieldPanel('content_after'),
    ]


    @route(r'^$')
    def booknow_page_route(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        cart = get_cart(request)
        rooms = Room.objects.filter(is_active=True)
        context['cart'] = cart
        context['rooms'] = rooms
        return render(request, 'home/book_page.html', context)

class CouponsPage(RoutablePageMixin, MyPage):

    max_count = 1
    template = "booking/view_coupon.html"

    coupons_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Header Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
    )

    coupons_image_alt = models.CharField(max_length=128, null=True, blank=True)

    content = StreamField(
        [
            ('section', myblocks.SectionBlock()),
        ],
        null=True,
        blank=True,
    )

    content_after = StreamField(

        [
            ('section', myblocks.SectionBlock()),
        ],
        null=True,
        blank=True,
    )

    coupons_pdf_title = models.CharField(max_length=32, null=True, blank=True)
    coupons_pdf_body = RichTextField(null=True, blank=True)
 
    content_panels = MyPage.content_panels + [
        StreamFieldPanel('content'),
        StreamFieldPanel('content_after'),
        MultiFieldPanel (
            heading="PDF Coupons Image",
            children = [
                FieldPanel("coupons_pdf_title"),
                FieldPanel("coupons_pdf_body"),
                ImageChooserPanel("coupons_image"),
                FieldPanel("coupons_image_alt"),
            ]
        )
    ]

    @route(r'^$')
    def coupons_page_route(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        cart = get_cart(request)
        try:
            online_coupon_family = ProductFamily.objects.get(slug='coupon-online')
            voucher_family = ProductFamily.objects.get(slug='coupon-voucher')
            online_coupon_form = AddProductToCartForm(family=online_coupon_family)
            voucher_form = AddProductToCartForm(family=voucher_family)
            context['cart'] = cart
            context['online_coupon_form'] = online_coupon_form
            context['voucher_form'] = voucher_form

        except Exception as e:
            print(e)

        print(context)
        return render(request, 'booking/view_coupon.html', context)
    # def serve(self, request):
    #     return  HttpResponseRedirect(reverse('booking:coupons'))


class CookieSettingsPage(LinkPage):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect('/cookies/')

class HomePage(MyPage):

    templates = "home/home_page.html"
    max_count = 1
    our_rooms_header = models.CharField(max_length=50, blank=True, null=True)
    our_rooms_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    online_header = models.CharField(max_length=50, blank=True, null=True)
    online_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    video_header = models.CharField(max_length=50, blank=True, null=True)
    video_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    offers_header = models.CharField(max_length=50, blank=True, null=True)
    offers_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    prices_header = models.CharField(max_length=50, blank=True, null=True)
    prices_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    reviews_header = models.CharField(max_length=50, blank=True, null=True)
    reviews_text = RichTextField(features=['bold', 'link'], blank=True, null=True)
    
    group_offers = StreamField(
        StreamBlock([
            ('offers', myblocks.OfferCardsBlock())
        ], 
        null=True,
        blank=True,
        max_num=1),
        null=True,
        blank=True,
    )

    faq = StreamField(
        [
            ('question', myblocks.AccordionBlock()),
        ],
        null=True,
        blank=True,
    )

    reviews = StreamField(
        StreamBlock([
                ('review_family', myblocks.ReviewCarouselBlock()),
            ],
            max_num=1,
        ),
        null=True,
        blank=True,
    )

    content_panels = MyPage.content_panels + [
        # ImageChooserPanel("header_image"),
        MultiFieldPanel(
            heading="Our Rooms",
            children=[
                FieldPanel('our_rooms_header'),
                FieldPanel('our_rooms_text'),
            ]
        ),
        MultiFieldPanel(
            heading="Online Games",
            children=[
                FieldPanel('online_header'),
                FieldPanel('online_text'),
            ]
        ),
        MultiFieldPanel(
            heading="Offers",
            children=[
                FieldPanel('offers_header'),
                FieldPanel('offers_text'),
            ]
        ),
        StreamFieldPanel('group_offers'),
        MultiFieldPanel(
            heading="Video",
            children=[
                FieldPanel('video_header'),
                FieldPanel('video_text'),
            ]
        ),
        MultiFieldPanel(
            heading="Prices",
            children=[
                FieldPanel('prices_header'),
                FieldPanel('prices_text'),
            ]
        ),
        MultiFieldPanel(
            heading="Reviews",
            children=[
                FieldPanel('reviews_header'),
                FieldPanel('reviews_text'),
            ]
        ),
        StreamFieldPanel('reviews'),
        StreamFieldPanel('faq'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['rooms'] = Room.objects.filter(is_active=True)
        context['cart'] = get_cart(request)
        context['coupons_page'] = CouponsPage.objects.first()
        context['booknow_page'] = BooknowPage.objects.first()
        return context


class RoomPage(MyPage):

    room = models.ForeignKey('booking.Room', related_name="room_page", null=True, blank=True, on_delete=models.SET_NULL)
    gallery = StreamField(
        StreamBlock([
            ('gallery', myblocks.ImageGalleryBlock())
        ],
        blank=True,
        null=True,
        max_num=1,
        ),
        null=True,
        blank=True,
    ) 

    video = models.CharField(max_length=50, null=True, blank=True)

    reviews = StreamField(
        StreamBlock([
            ('review_family', myblocks.ReviewCarouselBlock()),
            ],
            max_num=1,
        ),
        null=True,
        blank=True,
    )

    content_panels = MyPage.content_panels + [
        FieldPanel('room'),
        FieldPanel('video'),
        StreamFieldPanel('gallery'),
        StreamFieldPanel('reviews'),
    ]
    
