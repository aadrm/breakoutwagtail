from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    DateTimeBlock,
    FieldBlock,
    IntegerBlock,
    ListBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    TextBlock,
    URLBlock,
)
from wagtail.core.models import Orderable, Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
# from wagtailmarkdown.blocks import MarkdownBlock
from apps.wagtail.streams import blocks as myblocks
from wagtail.contrib.table_block.blocks import TableBlock


class ImageText(StructBlock):
    reverse = BooleanBlock(required=False)
    text = RichTextBlock()
    image = ImageChooserBlock()


class BodyBlock(StreamBlock):
    # h1 = CharBlock()
    # h2 = CharBlock()
    paragraph = RichTextBlock()
    # markdown = MarkdownBlock(icon="code")

    image_text = ImageText()

    mymaps = myblocks.MyMapsBlock()
    table = myblocks.CustomTableBlock()
    spacer = myblocks.SpacerBlock()
    
    # image_carousel = ListBlock(ImageChooserBlock())
    # thumbnail_gallery = ListBlock(ImageChooserBlock())