# Generated by Django 3.1.4 on 2021-03-20 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20210308_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='photo_alt',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Alt text'),
        ),
    ]
