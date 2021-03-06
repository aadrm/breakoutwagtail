# Generated by Django 3.1.4 on 2021-03-19 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0002_auto_20210319_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ReviewFamily',
                'verbose_name_plural': 'ReviewFamilys',
            },
        ),
        migrations.RemoveField(
            model_name='review',
            name='family',
        ),
        migrations.AddField(
            model_name='review',
            name='family',
            field=models.ManyToManyField(to='streams.ReviewFamily'),
        ),
    ]
