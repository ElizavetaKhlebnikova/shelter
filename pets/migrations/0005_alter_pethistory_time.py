# Generated by Django 3.2.12 on 2024-01-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_pethistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pethistory',
            name='time',
            field=models.DateField(),
        ),
    ]
