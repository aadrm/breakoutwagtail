# Generated by Django 3.1.4 on 2021-03-19 07:46

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_roompage_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.StructBlock([('review_family', wagtail.core.blocks.CharBlock(max_length=32))]))], blank=True, null=True),
        ),
    ]