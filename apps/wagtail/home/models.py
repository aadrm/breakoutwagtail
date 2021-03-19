from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse

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

from apps.booking.models import Room
from apps.booking.utils import get_cart

class HomePage(Page):

    templates = "hame/home_page.html"
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Header Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
    )

    our_rooms_header = models.CharField(max_length=50, blank=True, null=True)
    our_rooms_text = RichTextField(features=['bold', 'link'], blank=True, null=True)

    group_offers = StreamField(
        StreamBlock([
            ('offers', myblocks.OfferCardsBlock())
        ], 
        null=True,
        blank=True,
        min_num=1,
        max_num=1)
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

    content_panels = Page.content_panels + [
        # ImageChooserPanel("header_image"),
        MultiFieldPanel(
            heading="Our Rooms",
            children=[
                FieldPanel('our_rooms_header'),
                FieldPanel('our_rooms_text'),
            ]
        ),
        StreamFieldPanel('reviews'),
        StreamFieldPanel('group_offers'),
        StreamFieldPanel('faq'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['rooms'] = Room.objects.filter(is_active=True)
        context['cart'] = get_cart(request)
        return context


class RoomPage(Page):

    room = models.ForeignKey('booking.Room', null=True, blank=True, on_delete=models.SET_NULL)
    gallery = StreamField(
        StreamBlock([
            ('gallery', myblocks.ImageGalleryBlock())
        ],
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

    content_panels = Page.content_panels + [
        FieldPanel('room'),
        FieldPanel('video'),
        StreamFieldPanel('gallery'),
        StreamFieldPanel('reviews'),
    ]
    

class BooknowPage(Page):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect(reverse('booking:book'))

class CouponsPage(Page):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect(reverse('booking:coupons'))

class CookieSettingsPage(Page):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect('/cookies/')