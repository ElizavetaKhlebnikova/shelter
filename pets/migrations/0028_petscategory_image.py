# Generated by Django 3.2.12 on 2024-04-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0027_alter_requestforguardianship_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='petscategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images', verbose_name='Фото категории'),
        ),
    ]
