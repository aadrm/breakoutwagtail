# Generated by Django 3.1.4 on 2021-06-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0004_auto_20210306_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingsettings',
            name='slot_buffer_time',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]
