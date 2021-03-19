# Generated by Django 3.1.4 on 2021-03-14 17:10

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210314_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='group_offers',
            field=wagtail.core.fields.StreamField([('offers', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(max_length=48, required=False))])))]))]),
        ),
    ]