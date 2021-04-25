# Generated by Django 3.1.4 on 2021-04-25 19:51

import apps.wagtail.streams.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='body_de',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image_text', wagtail.core.blocks.StructBlock([('reverse', wagtail.core.blocks.BooleanBlock(required=False)), ('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('mymaps', apps.wagtail.streams.blocks.MyMapsBlock()), ('table', apps.wagtail.streams.blocks.CustomTableBlock()), ('spacer', apps.wagtail.streams.blocks.SpacerBlock())], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='body_en',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock()), ('image_text', wagtail.core.blocks.StructBlock([('reverse', wagtail.core.blocks.BooleanBlock(required=False)), ('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())])), ('mymaps', apps.wagtail.streams.blocks.MyMapsBlock()), ('table', apps.wagtail.streams.blocks.CustomTableBlock()), ('spacer', apps.wagtail.streams.blocks.SpacerBlock())], blank=True, null=True),
        ),
    ]
