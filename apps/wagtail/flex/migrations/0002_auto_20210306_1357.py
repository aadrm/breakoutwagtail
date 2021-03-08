# Generated by Django 3.1.4 on 2021-03-06 13:57

import apps.wagtail.streams.blocks
from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flexpage',
            name='content_de',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add a suitable section title', required=False)), ('uri_fragment', wagtail.core.blocks.CharBlock(help_text='uri fragment', required=False)), ('center_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('decorate_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('section_dark', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('stream', wagtail.core.blocks.StreamBlock([('rich_text', apps.wagtail.streams.blocks.RichTextBlock()), ('mymaps', apps.wagtail.streams.blocks.MyMapsBlock()), ('team_cards', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add a title for the cards if necessary, ', required=False)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Use a 400x300px picture,', required=True)), ('name', wagtail.core.blocks.CharBlock(max_length=48)), ('position', wagtail.core.blocks.TextBlock(max_length=48)), ('text', wagtail.core.blocks.TextBlock(max_length=256, required=False))])))])), ('spacer', apps.wagtail.streams.blocks.SpacerBlock()), ('horizontal_cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Use a 400x300px picture,', required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('subtitle', wagtail.core.blocks.TextBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.TextBlock(max_length=256, required=False)), ('link_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('link_url', wagtail.core.blocks.URLBlock(required=False)), ('link_text', wagtail.core.blocks.CharBlock(max_length=32, required=False)), ('reverse', wagtail.core.blocks.BooleanBlock(help_text='Place image to the right?', required=False))])))])), ('contact_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Contact us', help_text='Change if required for more appropriate text depending on the context', max_length=128, required=False)), ('background', wagtail.core.blocks.BooleanBlock(blank=True, default=False, help_text='leave unchecked for white background, check for dark background', null=True, required=False))])), ('table', wagtail.contrib.table_block.blocks.TableBlock())]))])), ('banner', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Please limit the image size to max 100KiB, recommended dimensions = 1280x450px', required=True))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flexpage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add a suitable section title', required=False)), ('uri_fragment', wagtail.core.blocks.CharBlock(help_text='uri fragment', required=False)), ('center_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('decorate_title', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('section_dark', wagtail.core.blocks.BooleanBlock(default=False, required=False)), ('stream', wagtail.core.blocks.StreamBlock([('rich_text', apps.wagtail.streams.blocks.RichTextBlock()), ('mymaps', apps.wagtail.streams.blocks.MyMapsBlock()), ('team_cards', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add a title for the cards if necessary, ', required=False)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Use a 400x300px picture,', required=True)), ('name', wagtail.core.blocks.CharBlock(max_length=48)), ('position', wagtail.core.blocks.TextBlock(max_length=48)), ('text', wagtail.core.blocks.TextBlock(max_length=256, required=False))])))])), ('spacer', apps.wagtail.streams.blocks.SpacerBlock()), ('horizontal_cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Use a 400x300px picture,', required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('subtitle', wagtail.core.blocks.TextBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.TextBlock(max_length=256, required=False)), ('link_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('link_url', wagtail.core.blocks.URLBlock(required=False)), ('link_text', wagtail.core.blocks.CharBlock(max_length=32, required=False)), ('reverse', wagtail.core.blocks.BooleanBlock(help_text='Place image to the right?', required=False))])))])), ('contact_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(default='Contact us', help_text='Change if required for more appropriate text depending on the context', max_length=128, required=False)), ('background', wagtail.core.blocks.BooleanBlock(blank=True, default=False, help_text='leave unchecked for white background, check for dark background', null=True, required=False))])), ('table', wagtail.contrib.table_block.blocks.TableBlock())]))])), ('banner', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Please limit the image size to max 100KiB, recommended dimensions = 1280x450px', required=True))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infopage',
            name='content_de',
            field=wagtail.core.fields.StreamField([('info_paragraph', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=128)), ('rich_text', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='infopage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('info_paragraph', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=128)), ('rich_text', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))]))], blank=True, null=True),
        ),
    ]
