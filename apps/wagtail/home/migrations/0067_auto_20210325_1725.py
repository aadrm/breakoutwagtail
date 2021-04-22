# Generated by Django 3.1.4 on 2021-03-25 17:25

from django.db import migrations
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0066_auto_20210324_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='group_offers',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('properties', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False)), ('noopener', wagtail.core.blocks.BooleanBlock(help_text='Select this for links that point to other websites', required=False)), ('new_tab', wagtail.core.blocks.BooleanBlock(required=False))], form_classname='inline_struct')), ('link_style', wagtail.core.blocks.StructBlock([('center', wagtail.core.blocks.BooleanBlock(required=False)), ('full_width', wagtail.core.blocks.BooleanBlock(required=False)), ('font_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False)), ('bg_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False))], form_classname='inline_struct'))]))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='group_offers_de',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('properties', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False)), ('noopener', wagtail.core.blocks.BooleanBlock(help_text='Select this for links that point to other websites', required=False)), ('new_tab', wagtail.core.blocks.BooleanBlock(required=False))], form_classname='inline_struct')), ('link_style', wagtail.core.blocks.StructBlock([('center', wagtail.core.blocks.BooleanBlock(required=False)), ('full_width', wagtail.core.blocks.BooleanBlock(required=False)), ('font_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False)), ('bg_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False))], form_classname='inline_struct'))]))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='group_offers_en',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('properties', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False)), ('noopener', wagtail.core.blocks.BooleanBlock(help_text='Select this for links that point to other websites', required=False)), ('new_tab', wagtail.core.blocks.BooleanBlock(required=False))], form_classname='inline_struct')), ('link_style', wagtail.core.blocks.StructBlock([('center', wagtail.core.blocks.BooleanBlock(required=False)), ('full_width', wagtail.core.blocks.BooleanBlock(required=False)), ('font_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False)), ('bg_colour', wagtail.core.blocks.ChoiceBlock(choices=[(1, 'Primary Green'), (2, 'Teal'), (3, 'Grey'), (4, 'Black'), (5, 'White')], required=False))], form_classname='inline_struct'))]))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='reviews_de',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='reviews_en',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roompage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
    ]