# Generated by Django 3.1.4 on 2021-03-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_de',
            field=models.TextField(null=True, verbose_name='Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='review_en',
            field=models.TextField(null=True, verbose_name='Review'),
        ),
    ]
