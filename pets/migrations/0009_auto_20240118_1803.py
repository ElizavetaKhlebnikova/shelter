# Generated by Django 3.2.12 on 2024-01-18 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0008_alter_petstatus_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pet',
            options={'verbose_name': 'подопечный', 'verbose_name_plural': 'Подопечные'},
        ),
        migrations.AlterModelOptions(
            name='pethistory',
            options={'verbose_name': 'История подопечного', 'verbose_name_plural': 'Истории подопечных'},
        ),
    ]
