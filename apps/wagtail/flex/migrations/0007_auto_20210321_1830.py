# Generated by Django 3.1.4 on 2021-03-21 18:30

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0006_formfield_formpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='intro_de',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formpage',
            name='intro_en',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
