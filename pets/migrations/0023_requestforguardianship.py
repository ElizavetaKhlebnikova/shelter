# Generated by Django 3.2.12 on 2024-03-24 19:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0022_auto_20240310_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForGuardianship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=256, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта для связи')),
                ('pet', models.CharField(max_length=256, verbose_name='Кличка подопечного')),
                ('city', models.CharField(max_length=256, verbose_name='Город проживания')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('goal', models.CharField(choices=[('None', 'не выбрано'), ('foster care', 'передержка'), ('home', 'дом')], max_length=20, verbose_name='Кем вы готовы стать для животного?')),
                ('other_pets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None, verbose_name='Если у вас уже есть питомцы, укажите, какие:')),
                ('other_pet', models.CharField(blank=True, max_length=256, null=True, verbose_name='Укажите вид вашего питомца')),
                ('conditions', models.BooleanField(verbose_name='Готовы ли вы выполнить все условия?')),
            ],
        ),
    ]
