# Generated by Django 3.1.4 on 2021-03-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description_de',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='room',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
