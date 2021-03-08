# Generated by Django 3.1.4 on 2021-03-06 09:20

import apps.booking.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=0, verbose_name='status')),
                ('items_before_checkout', models.SmallIntegerField(blank=True, null=True, verbose_name='items before purchase')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='CartCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Discount')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_coupons', to='booking.cart', verbose_name='Cart')),
            ],
            options={
                'verbose_name': 'CartCoupon',
                'verbose_name_plural': 'CartCoupons',
                'ordering': ['-coupon__is_upgrade', 'coupon__is_percent', 'coupon__is_apply_to_basket'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=32, verbose_name='Name')),
                ('phone', models.CharField(max_length=32, verbose_name='Phone')),
                ('email', models.EmailField(max_length=128, verbose_name='Email')),
                ('street', models.CharField(blank=True, max_length=128, null=True, verbose_name='Street')),
                ('post', models.CharField(blank=True, max_length=8, null=True, verbose_name='Post code')),
                ('city', models.CharField(blank=True, max_length=32, null=True, verbose_name='City')),
                ('company', models.CharField(blank=True, max_length=64, null=True, verbose_name='Company name')),
                ('is_terms', models.BooleanField(default=False, verbose_name='Accept terms')),
                ('is_privacy', models.BooleanField(default=False, verbose_name='Accept privacy')),
                ('order_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Order Placed')),
                ('order_int', models.SmallIntegerField(blank=True, editable=False, null=True, verbose_name='Order Number')),
                ('order_number', models.CharField(blank=True, editable=False, max_length=8, null=True, verbose_name='Order Number')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='display name')),
                ('method', models.CharField(max_length=16, verbose_name='method')),
            ],
            options={
                'verbose_name': 'PaymentMethod',
                'verbose_name_plural': 'PaymentMethods',
            },
        ),
        migrations.CreateModel(
            name='ProductFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Product Family')),
                ('is_coupon', models.BooleanField(default=False, verbose_name='Is coupon')),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Shipping cost')),
                ('payment_methods', models.ManyToManyField(to='booking.PaymentMethod')),
            ],
            options={
                'verbose_name': 'ProductFamily',
                'verbose_name_plural': 'ProductFamilies',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/rooms', verbose_name='Image')),
                ('red', models.SmallIntegerField(default=255, verbose_name='Red')),
                ('green', models.SmallIntegerField(default=255, verbose_name='Green')),
                ('blue', models.SmallIntegerField(default=255, verbose_name='Blue')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('dow', models.PositiveSmallIntegerField(verbose_name='Day of Week')),
                ('start_time', models.TimeField(verbose_name='Start Time')),
                ('interval', models.PositiveSmallIntegerField(default=30, verbose_name='Interval')),
                ('duration', models.PositiveSmallIntegerField(default=60, verbose_name='Duration')),
                ('instances', models.PositiveSmallIntegerField(verbose_name='Instances')),
                ('product_family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.productfamily', verbose_name='ProductFamily')),
            ],
            options={
                'ordering': ['product_family__room', 'start_date', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('duration', models.PositiveSmallIntegerField(default=60, verbose_name='Duration')),
                ('interval', models.PositiveSmallIntegerField(default=30, verbose_name='interval')),
                ('protect', models.BooleanField(null=True, verbose_name='protect')),
                ('product_family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.productfamily', verbose_name='ProductFamily')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room', verbose_name='room')),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='slots', to='booking.schedule', verbose_name='schedule')),
            ],
            options={
                'ordering': ['room', 'start'],
            },
        ),
        migrations.AddField(
            model_name='productfamily',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.room', verbose_name='Room'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Product')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price')),
                ('players', models.SmallIntegerField(blank=True, null=True, verbose_name='Players')),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='booking.productfamily', verbose_name='Family')),
                ('upgrade', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='degrade', to='booking.product', verbose_name='upgrade')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='booking.invoice')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.paymentmethod', verbose_name='Payment Method'),
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='reference')),
                ('code', models.SlugField(blank=True, max_length=32, unique=True, verbose_name='code')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='discount amount')),
                ('is_percent', models.BooleanField(default=False, verbose_name='apply as percent')),
                ('is_apply_to_basket', models.BooleanField(default=False, verbose_name='apply to entire basket')),
                ('is_individual_use', models.BooleanField(default=True, verbose_name='cannot be used in conjunction with other coupons')),
                ('is_overrule_individual_use', models.BooleanField(default=False, verbose_name='can be used with individual use coupons')),
                ('is_upgrade', models.BooleanField(default=False, verbose_name='Upgrades the item')),
                ('used_times', models.IntegerField(default=0, verbose_name='Used times')),
                ('use_limit', models.IntegerField(default=1, verbose_name='Usage limit')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Created')),
                ('expiry', models.DateField(blank=True, default=apps.booking.models.Coupon.now_plus_time, null=True, verbose_name='Expiration date')),
                ('minimum_spend', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Minimum spend')),
                ('dow_valid', models.PositiveSmallIntegerField(default=127, verbose_name='Days Valid')),
                ('product_excluded', models.ManyToManyField(blank=True, related_name='product_exclude', to='booking.Product', verbose_name='exclude product')),
                ('product_families_excluded', models.ManyToManyField(blank=True, related_name='product_family_exclude', to='booking.ProductFamily', verbose_name=' exclude families')),
                ('product_families_included', models.ManyToManyField(blank=True, related_name='product_family_include', to='booking.ProductFamily', verbose_name=' include families')),
                ('product_included', models.ManyToManyField(blank=True, related_name='product_include', to='booking.Product', verbose_name='include product')),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=0, verbose_name='status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Price')),
                ('marked_shipped', models.DateTimeField(blank=True, null=True, verbose_name='Shipped')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='booking.cart', verbose_name='Cart')),
                ('cart_coupons', models.ManyToManyField(blank=True, related_name='cart_items', to='booking.CartCoupon', verbose_name='coupons')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to='booking.coupon')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.product')),
                ('slot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to='booking.slot', verbose_name='slot')),
            ],
        ),
        migrations.AddField(
            model_name='cartcoupon',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.coupon', verbose_name='Cart Coupon'),
        ),
        migrations.AddField(
            model_name='cart',
            name='invoice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='booking.invoice', verbose_name='Invoice'),
        ),
    ]