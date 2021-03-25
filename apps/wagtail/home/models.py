from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render

from wagtail.core import blocks
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel, ImageFieldComparison
from wagtail.core.fields import StreamField, StreamBlock, BlockField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from apps.wagtail.streams import blocks as myblocks

from apps.booking.models import Room

from django.utils.translation import ugettext_lazy as _

from apps.booking.models import Room, ProductFamily
from apps.booking.forms import AddProductToCartForm 
from apps.booking.utils import get_cart

class MyPage(Page):

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

    extra_schema = models.TextField(null=True, blank=True)

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
        FieldPanel('extra_schema'),
    ]


class LinkPage(MyPage):

    class Meta:
        abstract = True
    
    content_panels = [FieldPanel('title')]
    promote_panels = [
        FieldPanel('slug')

    ]


class BooknowPage(RoutablePageMixin, LinkPage):

    max_count = 1
    template = "booking/view_book.html"

    @route(r'^$')
    def booknow_page_route(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        cart = get_cart(request)
        rooms = Room.objects.filter(is_active=True)
        context['cart'] = cart
        context['rooms'] = rooms
        return render(request, 'booking/view_book.html', context)

class CouponsPage(RoutablePageMixin, MyPage):

    max_count = 1
    template = "booking/view_coupon.html"

    @route(r'^$')
    def coupons_page_route(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        cart = get_cart(request)
        try:
            online_coupon_family = ProductFamily.objects.get(name='CouponOnline')
            voucher_family = ProductFamily.objects.get(name='CouponVoucher')
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
    
