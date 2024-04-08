# Generated by Django 3.2.12 on 2024-01-30 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0013_alter_news_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='pet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pets.pet', verbose_name='Подопечный, на которого даётся ссылка'),
        ),
    ]
