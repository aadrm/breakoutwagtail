# Generated by Django 3.1.4 on 2021-03-20 11:16

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0035_auto_20210320_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='booknowpage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Header Image'),
        ),
        migrations.AddField(
            model_name='booknowpage',
            name='header_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booknowpage',
            name='seo_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Seo Image'),
        ),
        migrations.AddField(
            model_name='booknowpage',
            name='seo_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='couponspage',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Header Image'),
        ),
        migrations.AddField(
            model_name='couponspage',
            name='header_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='couponspage',
            name='seo_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Seo Image'),
        ),
        migrations.AddField(
            model_name='couponspage',
            name='seo_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='seo_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roompage',
            name='header_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roompage',
            name='seo_image_alt',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='homepage',
            name='group_offers',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False))]))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='group_offers_de',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False))]))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='group_offers_en',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('icon', wagtail.core.blocks.RawHTMLBlock(required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=48, required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'link'], required=False)), ('link', wagtail.core.blocks.StructBlock([('page_link', wagtail.core.blocks.PageChooserBlock(required=False)), ('url_link', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(max_length=64, required=False))]))])))]))], blank=True, null=True),
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
