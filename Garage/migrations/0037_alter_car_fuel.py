# Generated by Django 3.2 on 2022-04-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0036_alter_car_mileage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='fuel',
            field=models.PositiveIntegerField(choices=[(1, 'Бензин'), (2, 'Дизель'), (3, 'Газ'), (4, 'Газ/Бензин'), (5, 'Гибрид'), (6, 'Электро'), (7, 'Газ метан'), (8, 'Газ пропан-бутан'), (9, 'Другое')], default='Тип топлива', verbose_name='Топливо'),
        ),
    ]
