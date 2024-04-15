# Generated by Django 3.2.12 on 2024-04-15 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0035_pethistory_send_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pethistory',
            name='date',
            field=models.DateField(verbose_name='Дата*'),
        ),
        migrations.AlterField(
            model_name='pethistory',
            name='node',
            field=models.TextField(verbose_name='Новость из жизни подопечного*'),
        ),
        migrations.AlterField(
            model_name='pethistory',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet', verbose_name='Кличка подопечного*'),
        ),
        migrations.AlterField(
            model_name='pethistory',
            name='title',
            field=models.CharField(default='Новое событие в жизни*', max_length=60, verbose_name='Заголовок новости'),
        ),
    ]
