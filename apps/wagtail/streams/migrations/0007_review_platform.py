# Generated by Django 3.1.4 on 2021-03-19 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0006_auto_20210319_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='streams.reviewplatform'),
        ),
    ]