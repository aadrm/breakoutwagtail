# Generated by Django 3.1.4 on 2021-07-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0006_auto_20210615_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingsettings',
            name='booking_notification_emails',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
