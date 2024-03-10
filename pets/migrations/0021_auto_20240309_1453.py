# Generated by Django 3.2.12 on 2024-03-09 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0020_petimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='needs',
            field=models.TextField(blank=True, null=True, verbose_name='Нужды в настоящий момент'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True),
        ),
    ]
