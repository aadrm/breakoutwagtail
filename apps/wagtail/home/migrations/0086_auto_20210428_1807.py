# Generated by Django 3.1.4 on 2021-04-28 18:07

from django.db import migrations, models
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0085_auto_20210427_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='booknowpage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='cookiesettingspage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='couponspage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='roompage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
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