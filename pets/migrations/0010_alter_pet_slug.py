# Generated by Django 3.2.12 on 2024-01-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0009_auto_20240118_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='slug',
            field=models.SlugField(default='', null=True),
        ),
    ]
