"""flexible page"""
from django.db import models

from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField

from apps.wagtail.streams import blocks

class FlexPage(Page):
    """Flexible page class""" 

    template = "flex/flex_page.html"

    header_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Header Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ('section', blocks.SectionBlock()),
            ('banner', blocks.ImgBannerSeparator()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("header_image"),
        StreamFieldPanel("content"),
    ]


    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"


class InfoPage(Page):
    """Info page class"""
    template = "flex/info_page.html"

    header_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        verbose_name=_("Banner Image"), 
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="limit the file size to 200kb, recommended dimensions 1200x500",
    )

    is_numbered = models.BooleanField(_("Enumerate Paragraphs"), default=False)

    content = StreamField(
        [
            ("info_paragraph", blocks.InfoParagraphBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('is_numbered'),
        StreamFieldPanel('content'),

    ]

    class Meta:
        verbose_name = "Info Page"
        verbose_name_plural = "Info Pages"

