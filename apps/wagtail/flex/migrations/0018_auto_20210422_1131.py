# Generated by Django 3.1.4 on 2021-04-22 11:31

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0009_wagtaillanguage'),
        ('flex', '0017_auto_20210328_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='flexpage',
            name='translations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='menus.WagtailLanguage'),
        ),
        migrations.AddField(
            model_name='formpage',
            name='translations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='menus.WagtailLanguage'),
        ),
        migrations.AddField(
            model_name='infopage',
            name='translations',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='menus.WagtailLanguage'),
        ),
    ]