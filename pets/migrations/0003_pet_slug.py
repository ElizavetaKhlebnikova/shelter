# Generated by Django 3.2.12 on 2024-01-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_basket_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
