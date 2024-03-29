# Generated by Django 3.2.10 on 2022-11-26 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0025_alter_cart_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Coupon', 'verbose_name_plural': 'Coupons'},
        ),
        migrations.AddField(
            model_name='cartitem',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=999, max_digits=8, verbose_name='Preis'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preis'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='created',
            field=models.DateTimeField(auto_now=True, verbose_name='Created'),
        ),
    ]
