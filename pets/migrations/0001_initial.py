# Generated by Django 3.2.12 on 2023-12-13 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'категорию',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='PetStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Кличка животного')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='product_images', verbose_name='Фото животного')),
                ('is_hospitalized', models.BooleanField(default=False, verbose_name='Находится в стационаре')),
                ('gender', models.CharField(choices=[('m', 'Мальчик'), ('f', 'Девочка')], default='m', max_length=1, verbose_name='Пол животного')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.petscategory', verbose_name='Вид животного')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.petstatus', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'животное',
                'verbose_name_plural': 'животные',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet')),
            ],
        ),
    ]
