# Generated by Django 3.1.4 on 2021-04-23 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20210422_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfamily',
            name='name_de',
            field=models.CharField(max_length=16, null=True, verbose_name='Product Family'),
        ),
        migrations.AddField(
            model_name='productfamily',
            name='name_en',
            field=models.CharField(max_length=16, null=True, verbose_name='Product Family'),
        ),
        migrations.AddField(
            model_name='productfamily',
            name='slug',
            field=models.CharField(default='slug', max_length=32, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productfamily',
            name='name',
            field=models.CharField(max_length=16, verbose_name='Product Family'),
        ),
    ]
