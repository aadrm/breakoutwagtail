# Generated by Django 3.2.10 on 2022-05-30 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0022_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=8, verbose_name='Preis'),
        ),
    ]
