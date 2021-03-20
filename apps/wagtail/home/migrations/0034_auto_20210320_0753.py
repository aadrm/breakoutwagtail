# Generated by Django 3.1.4 on 2021-03-20 07:53

from django.db import migrations
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20210319_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='group_offers_de',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock()), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False))]))])))]))], null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='group_offers_en',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock()), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False))]))])))]))], null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='reviews_de',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='reviews_en',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roompage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
    ]