# Generated by Django 3.1.4 on 2021-03-21 19:09

from django.db import migrations
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_auto_20210321_1830'),
    ]

    operations = [
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
