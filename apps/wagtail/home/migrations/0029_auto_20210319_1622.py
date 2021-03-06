# Generated by Django 3.1.4 on 2021-03-19 16:22

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('home', '0028_auto_20210319_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roompage',
            name='reviews',
            field=wagtail.core.fields.StreamField([('review_family', wagtail.core.blocks.MultipleChoiceBlock(choices=django.db.models.query.QuerySet.values_list))], blank=True, null=True),
        ),
    ]
