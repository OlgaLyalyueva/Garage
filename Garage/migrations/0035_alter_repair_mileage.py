# Generated by Django 3.2 on 2022-02-17 09:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0034_alter_repair_mileage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='mileage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000000)], verbose_name='Пробег'),
        ),
    ]
