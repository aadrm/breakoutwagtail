# Generated by Django 3.1.4 on 2021-05-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_cart_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
    ]
