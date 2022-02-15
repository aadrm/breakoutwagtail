# Generated by Django 3.2.10 on 2022-02-15 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_product_value'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Gutschein', 'verbose_name_plural': 'Gutscheine'},
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preis'),
        ),
        migrations.AlterField(
            model_name='product',
            name='players',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Spieler'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preis'),
        ),
        migrations.AlterField(
            model_name='product',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Wert'),
        ),
        migrations.AlterField(
            model_name='productfamily',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.room', verbose_name='Raum'),
        ),
    ]