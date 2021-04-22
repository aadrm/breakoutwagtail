# Generated by Django 3.1.4 on 2021-03-25 18:29

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_coupondocument_coupontemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupondocument',
            name='docs',
            field=modelcluster.fields.ParentalKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='menus.menu'),
            preserve_default=False,
        ),
    ]