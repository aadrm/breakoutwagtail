from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel, ImageFieldComparison
from wagtail.core.fields import StreamField, StreamBlock, BlockField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from apps.wagtail.streams import blocks

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



    faq = StreamField(
        [
            ('question', blocks.AccordionBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("header_image"),
        StreamFieldPanel('faq'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['rooms'] = Room.objects.filter(is_active=True)
        context['cart'] = get_cart(request)
        return context



class BooknowPage(Page):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect(reverse('booking:book'))


class CookieSettingsPage(Page):

    max_count = 1
    def serve(self, request):
        return HttpResponseRedirect('/cookies/')