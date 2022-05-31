# Generated by Django 3.2.10 on 2022-05-31 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_alter_cartitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Subtotal'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Total'),
        ),
    ]