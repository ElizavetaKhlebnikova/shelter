# Generated by Django 3.2.12 on 2024-04-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image_url',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='Текст новости'),
        ),
    ]
