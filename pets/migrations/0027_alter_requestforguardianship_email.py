# Generated by Django 3.2.12 on 2024-04-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0026_auto_20240324_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestforguardianship',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Электронная почта для связи'),
        ),
    ]
