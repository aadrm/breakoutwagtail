# Generated by Django 3.1.4 on 2021-03-22 19:02

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0008_auto_20210321_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpage',
            name='submitted_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='formpage',
            name='submitted_title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='submitted title'),
        ),
    ]
