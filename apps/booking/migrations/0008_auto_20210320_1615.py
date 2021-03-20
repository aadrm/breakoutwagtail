# Generated by Django 3.1.4 on 2021-03-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_room_photo_alt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='blue',
        ),
        migrations.RemoveField(
            model_name='room',
            name='green',
        ),
        migrations.RemoveField(
            model_name='room',
            name='red',
        ),
        migrations.AddField(
            model_name='room',
            name='theme_colour',
            field=models.CharField(default='999999', max_length=6, verbose_name='Colour Hexagesimal'),
        ),
    ]
