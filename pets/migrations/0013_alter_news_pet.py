# Generated by Django 3.2.12 on 2024-01-30 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0012_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='pet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pets.pet', verbose_name='Подопечный, на которого даётся ссылка'),
        ),
    ]
