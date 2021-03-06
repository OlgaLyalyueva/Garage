# Generated by Django 3.2 on 2022-02-14 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0030_alter_improvement_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='price',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Стоимость страховки'),
        ),
    ]
