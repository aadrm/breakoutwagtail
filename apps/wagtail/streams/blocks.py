""" Stream fields live here """
from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from wagtail.images import blocks as images_blocks

from wagtail.contrib.table_block.blocks import TableBlock

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
    
    page_link = blocks.PageChooserBlock(required=False)
    url_link = blocks.URLBlock(required=False)
    text = blocks.CharBlock(max_length=32, required=True)

    class Meta:
        icon = 'user'


class SubtitleBlock(blocks.StructBlock):
    """ Title block and nothing else """

    subtitle = blocks.CharBlock(required=True, help_text='Add your subtitle')

    class Meta: 
        template = 'streams/subtitle_block.html'
        icon = 'title'
        label = 'Subtitle'


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


class HorizontalCardsBlock(blocks.StructBlock):
    """ Cards with image and title else """

    # title = blocks.CharBlock(required=False, help_text='Add a title for the cards if necessary, ')

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', images_blocks.ImageChooserBlock(
                    required=True,
                    help_text='Use a 400x300px picture,'
                    )),
                ('title', blocks.CharBlock(max_length=48, required=False)),
                ('subtitle', blocks.TextBlock(max_length=48, required=False)),
                ('text', blocks.TextBlock(max_length=256, required=False)),
                ('link_page', blocks.PageChooserBlock(required=False)),
                ('link_url', blocks.URLBlock(required=False)),
                ('link_text', blocks.CharBlock(max_length=32, required=False)),
                ('reverse', blocks.BooleanBlock(required=False, help_text="Place image to the right?"))
            ]
        )
    )

    class Meta: 
        template = 'streams/fullwidthcards_block.html'
        icon = 'placeholder'
        label = 'Full width cards'



class TeamCardsBlock(blocks.StructBlock):
    """ Cards with image and title else """

    title = blocks.CharBlock(required=False, help_text='Add a title for the cards if necessary, ')

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', images_blocks.ImageChooserBlock(
                    required=True,
                    help_text='Use a 400x300px picture,'
                    )),
                ('name', blocks.CharBlock(max_length=48)),
                ('position', blocks.TextBlock(max_length=48)),
                ('text', blocks.TextBlock(max_length=256, required=False)),
            ]
        )
    )

    class Meta: 
        template = 'streams/team_block.html'
        icon = 'fa-address-card'
        label = 'Staff cards'


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

    image = images_blocks.ImageChooserBlock(required=True, help_text="Please limit the image size to max 40KiB, recommended dimensions = 512x288px")
    title = blocks.CharBlock(max_length=48, required=False)
    sub_title = blocks.CharBlock(max_length=48, required=False)
    text = blocks.TextBlock(max_length=1024, required=False)
    button = blocks.PageChooserBlock(required=False)
    button_text = blocks.CharBlock(max_length=32, required=True, default="Lear more")
    #         ('button_url', blocks.PageChooserBlock(required=False, helptext="button page has priority")),

    class Meta: 
        template = 'streams/service_block.html'
        icon = 'placeholder'
        label = 'Services'


class ImgBannerSeparator(blocks.StructBlock):
    """Image separator"""
    image = images_blocks.ImageChooserBlock(required=True, help_text="Please limit the image size to max 100KiB, recommended dimensions = 1280x450px")

    class Meta: 
        template = 'streams/banner_block.html'
        icon = 'image'
        label = 'Image separator'


class InfoParagraphBlock(blocks.StructBlock):
    """Info Paragraph block class"""

    title = blocks.CharBlock(max_length=128)
    rich_text = blocks.RichTextBlock(
        features = [
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
        label = 'Google my maps'


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, help_text='Add a suitable section title')
    uri_fragment = blocks.CharBlock(required=False, help_text='uri fragment')
    center_title = blocks.BooleanBlock(default=False, required=False)
    decorate_title = blocks.BooleanBlock(default=False, required=False)
    section_dark = blocks.BooleanBlock(default=False, required=False)
    stream = blocks.StreamBlock(
        [
            ('rich_text', RichTextBlock()),
            ('mymaps', MyMapsBlock()),
            ('team_cards', TeamCardsBlock()),
            ('spacer', SpacerBlock()),
            ('horizontal_cards', HorizontalCardsBlock()),
            ('contact_block', ContactBlock()),
            ('table', TableBlock()),
        ],
    )    
    class Meta:
        template = 'streams/section_block.html'
        icon = 'doc-full'
        label = 'Section'