# Generated by Django 3.0.3 on 2020-03-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0005_auto_20200316_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionresponse',
            name='text',
            field=models.TextField(blank=True, max_length=600, verbose_name='text'),
        ),
    ]
