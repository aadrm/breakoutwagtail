# Generated by Django 3.1.4 on 2021-03-21 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_auto_20210321_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='fixed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
