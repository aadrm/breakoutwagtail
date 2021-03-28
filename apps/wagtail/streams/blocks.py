""" Stream fields live here """
from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from django.db import models
from django import forms
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images import blocks as images_blocks
from wagtail.contrib.table_block.blocks import TableBlock
from .models import ReviewFamily, Review, Colour


class ElementBlock(blocks.StructBlock):

    style = blocks.StructBlock(
        [
            ('font_colour', blocks.ChoiceBlock(
                choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
            ('bg_colour', blocks.ChoiceBlock(
                choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
            ('shadow', blocks.IntegerBlock(required=False)),
            ('max_width_outer', blocks.IntegerBlock(required=False)),
        ], form_classname='inline_struct'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            context['value']['style']['font_colour'] = Colour.objects.get(
                pk=context['value']['style']['font_colour']).hex_code
        except Exception:
            pass
        try:
            context['value']['style']['bg_colour'] = Colour.objects.get(
                pk=context['value']['style']['bg_colour']).hex_code
        except Exception:
            pass
        return context

    class Meta:
        template = 'streams/element_block.html'


class ElementBlockExtended(ElementBlock):
    style = blocks.StructBlock(
        [
            ('font_colour', blocks.ChoiceBlock(
                choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
            ('bg_colour', blocks.ChoiceBlock(
                choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
            ('shadow', blocks.IntegerBlock(required=False)),
            ('max_width_inner', blocks.IntegerBlock(required=False)),

        ], form_classname='inline_struct'
    )


class SubtitleBlock(blocks.StructBlock):
    """ Title block with shord description """

    title = blocks.StructBlock(
        [
            ('subtitle', blocks.CharBlock(required=False)),
            ('uri_fragment', blocks.CharBlock(required=False)),
            ('center_title', blocks.BooleanBlock(default=False, required=False)),
            ('decorate_title', blocks.BooleanBlock(default=False, required=False)),
            ('title_level', blocks.ChoiceBlock(required=False, choices=(('h2','h2'),('h3','h3'),('h4','h4')))),
            ('title_colour', blocks.ChoiceBlock(
                choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
        ], form_classname='inline_struct', label="Properties"
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        print(context['value']['title']['title_colour'])
        try:
            context['value']['title']['title_colour'] = Colour.objects.get(
                pk=context['value']['title']['title_colour']).hex_code
        except Exception:
            pass
        return context

    class Meta:
        template = 'streams/subtitle_block.html'
        icon = 'title'
        label = 'Subtitle'

class SubtitleTextBlock(SubtitleBlock):
    richtext = blocks.RichTextBlock(required=False)

class CollectionBlock(ElementBlockExtended):
    title = SubtitleTextBlock(required=False, help_text='Block title')
    children = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('children', ElementBlock()),
            ]
        )
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['value']['h_value'] = 'h3'
        return context

    class Meta:
        template = 'streams/collection_block.html'


class ImageTextBlock(ElementBlock):
    image = images_blocks.ImageChooserBlock(required=True)
    text = blocks.RichTextBlock()

    class Meta:
        template = 'streams/image_text_block.html'
        icon = 'placeholder'
        label = 'Image | Text'


class SpacerBlock(blocks.IntegerBlock):
    def __init__(self, *args, **kwargs):
        self.help_text = 'Enter height in px'
        super(SpacerBlock, self).__init__(*args, **kwargs)

    class Meta:
        template = 'streams/spacer_block.html'
        icon = 'horizontalrule'
        label = 'spacer'


class LinkBlock(blocks.StructBlock):
    """Link block"""

    properties = blocks.StructBlock([
        ('page_link', blocks.PageChooserBlock(required=False)),
        ('url_link', blocks.URLBlock(required=False)),
        ('button_text', blocks.CharBlock(max_length=64, required=False)),
        ('noopener', blocks.BooleanBlock(required=False,
                                         help_text="Select this for links that point to other websites")),
        ('new_tab', blocks.BooleanBlock(required=False)),
    ],
        form_classname='inline_struct'
    )
    link_style = blocks.StructBlock([
        ('center', blocks.BooleanBlock(required=False)),
        ('full_width', blocks.BooleanBlock(required=False)),
        ('font_colour', blocks.ChoiceBlock(
            choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
        ('bg_colour', blocks.ChoiceBlock(
            choices=Colour.objects.all().values_list('pk', 'name'), required=False)),
    ],
        form_classname='inline_struct'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            context['value']['link_style']['font_colour'] = Colour.objects.get(
                pk=context['value']['link_style']['font_colour']).hex_code
        except Exception:
            pass
        try:
            context['value']['link_style']['bg_colour'] = Colour.objects.get(
                pk=context['value']['link_style']['bg_colour']).hex_code
        except Exception:
            pass
        return context

    class Meta:
        template = 'streams/link_block.html'
        label = 'Link'
        icon = 'user'



class RichTextBlock(blocks.RichTextBlock):
    """ Rich text block with all the features."""

    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'doc-full'
        label = 'Rich text'


class SimpleRichTextBlock(blocks.RichTextBlock):
    """ Rich text block with limited features """

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link',
        ]

    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'edit'
        label = 'Simple RichText'


class ReviewCarouselBlock(blocks.MultipleChoiceBlock):

    choices = ReviewFamily.objects.all().values_list

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['reviews'] = Review.objects.filter(
            family__in=context['value']).distinct()
        return context

    class Meta:
        template = 'streams/reviews_carousel_block.html'
        icon = 'image'
        label = 'Reviews'


class ImageGalleryBlock(blocks.StructBlock):
    gallery = blocks.ListBlock(
        blocks.StructBlock([
            ('image', images_blocks.ImageChooserBlock()),
            ('alt', blocks.CharBlock()),
        ])
    )

    class Meta:
        template = 'streams/gallery_block.html'
        icon = 'image'
        label = 'Image Gallery'


class CardBlock(ElementBlockExtended):
    image = images_blocks.ImageChooserBlock(
        required=True,
        help_text='Use a 400x300px picture,'
    )
    image_alt = blocks.CharBlock(max_length=128, required=False)
    title = blocks.CharBlock(max_length=48, required=False)
    subtitle = blocks.CharBlock(max_length=48, required=False)
    text = blocks.TextBlock(required=False)
    link = LinkBlock()

    class Meta:
        template = 'streams/cards/card_block.html'


class HorizontalCardBlock(CardBlock):
    flip = blocks.BooleanBlock(required=False, default=False)


class VerticalCardsBlock(CollectionBlock):
    """ Cards with image and title else """

    children = blocks.ListBlock(
        CardBlock(),
    )

    class Meta:
        template = 'streams/cards/vertical_cards_block.html'
        icon = 'fa-address-card'
        label = 'Vertical Cards'


class HorizontalCardsBlock(CollectionBlock):
    """ Cards with image and title else """

    children = blocks.ListBlock(
        HorizontalCardBlock(),
    )

    class Meta:
        template = 'streams/cards/horizontal_cards_block.html'
        icon = 'placeholder'
        label = 'Horizontal cards'


class OfferCardsBlock(blocks.StructBlock):
    """ Cards with image title subtitle and text """

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('icon', blocks.RawHTMLBlock(required=False)),
                ('title', blocks.CharBlock(max_length=48, required=False)),
                ('text', blocks.RichTextBlock(
                    features=['bold', 'link'], required=False)),
                ('link', LinkBlock()),
            ]
        )
    )

    class Meta:
        template = 'streams/offer_block.html'
        icon = 'fa-address-card'
        label = 'Offer Card Block'


class ServicesCard(blocks.StructBlock):
    """ Services cards """
    # blocks.StructBlock(
    #     [
    #         ('image', images_blocks.ImageChooserBlock(required=True)),
    #         ('title', blocks.CharBlock(max_length=48)),
    #         ('text', blocks.TextBlock(max_length=256)),
    #         ('button_page', blocks.PageChooserBlock(required=False)),
    #         ('button_url', blocks.PageChooserBlock(required=False, helptext="button page has priority")),
    #     ]
    # )

    image = images_blocks.ImageChooserBlock(
        required=True, help_text="Please limit the image size to max 40KiB, recommended dimensions = 512x288px")
    title = blocks.CharBlock(max_length=48, required=False)
    sub_title = blocks.CharBlock(max_length=48, required=False)
    text = blocks.TextBlock(max_length=1024, required=False)
    button = blocks.PageChooserBlock(required=False)
    button_text = blocks.CharBlock(
        max_length=32, required=True, default="Lear more")
    #         ('button_url', blocks.PageChooserBlock(required=False, helptext="button page has priority")),

    class Meta:
        template = 'streams/service_block.html'
        icon = 'placeholder'
        label = 'Services'


class ImgBannerSeparator(blocks.StructBlock):
    """Image separator"""
    image = images_blocks.ImageChooserBlock(
        required=True, help_text="Please limit the image size to max 100KiB, recommended dimensions = 1280x450px")

    class Meta:
        template = 'streams/banner_block.html'
        icon = 'image'
        label = 'Image separator'


class InfoParagraphBlock(blocks.StructBlock):
    """Info Paragraph block class"""

    title = blocks.CharBlock(max_length=128)
    rich_text = blocks.RichTextBlock(
        features=[
            'h3', 'h4', 'h5', 'h6',
            'bold', 'italic',
            'ol', 'ul',
            'hr',
            'link',
            'document-link',
        ]
    )

    class Meta:
        template = 'streams/info_paragraph.html'
        icon = 'pilcrow'
        label = 'Paragraph'


class AccordionBlock(InfoParagraphBlock):
    class Meta:
        template = 'streams/accordion_block.html'
        icon = 'pilcrow'
        label = 'Paragraph'


class ContactBlock(blocks.StructBlock):
    """Contact Block"""
    title = blocks.CharBlock(
        max_length=128,
        default='Contact us',
        required=False,
        help_text='Change if required for more appropriate text depending on the context'
    )
    background = blocks.BooleanBlock(
        default=False,
        required=False,
        blank=True,
        null=True,
        help_text='leave unchecked for white background, check for dark background'
    )

    class Meta:
        template = 'streams/contact_block.html'
        icon = 'fa-phone-square'
        label = 'contact block'


class MyMapsBlock(blocks.URLBlock):

    class Meta:
        template = 'streams/mymaps_block.html'
        icon = 'site'
        label = 'MyMaps block'


class IframeBlock(blocks.URLBlock):

    class Meta:
        template = 'stream/iframe_blocks.html'
        icon = 'site'
        label = 'iframe block'


class SectionBlock(ElementBlockExtended):
    title = SubtitleBlock(
        required=False, help_text='Add a suitable section title')
    is_section = True
    stream = blocks.StreamBlock(
        [
            # ('subtitle_block', SubtitleBlock()),
            ('collection_test', CollectionBlock()),
            ('rich_text', RichTextBlock()),
            ('mymaps', MyMapsBlock()),
            ('cards', VerticalCardsBlock()),
            ('spacer', SpacerBlock()),
            ('image_text', ImageTextBlock()),
            ('horizontal_cards', HorizontalCardsBlock()),
            # ('contact_block', ContactBlock()),
            ('table', TableBlock()),
        ],
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['value']['is_section'] = True
        return context

    class Meta:
        template = 'streams/section_block.html'
        icon = 'doc-full'
        label = 'Section'
