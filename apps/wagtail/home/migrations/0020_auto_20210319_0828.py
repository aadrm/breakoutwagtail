# Generated by Django 3.1.4 on 2021-03-19 08:28

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_homepage_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.StructBlock([]))], blank=True, null=True),
        ),
    ]
