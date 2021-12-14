# Generated by Django 3.2.10 on 2021-12-14 11:34

from django.db import migrations, models
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0096_auto_20211214_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponspage',
            name='coupons_pdf_body',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='couponspage',
            name='coupons_pdf_title',
            field=models.CharField(blank=True, max_length=32, null=True),
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
