# Generated by Django 3.1.4 on 2021-04-28 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0020_auto_20210427_0645'),
    ]

    operations = [
        migrations.AddField(
            model_name='flexpage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='formpage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
        migrations.AddField(
            model_name='infopage',
            name='keywords',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Keywords'),
        ),
    ]
