# Generated by Django 3.1.4 on 2021-03-07 07:45

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_homepage_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='faq_de',
            field=wagtail.core.fields.StreamField([('question', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=128)), ('rich_text', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='faq_en',
            field=wagtail.core.fields.StreamField([('question', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=128)), ('rich_text', wagtail.core.blocks.RichTextBlock(features=['h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link']))]))], blank=True, null=True),
        ),
    ]
