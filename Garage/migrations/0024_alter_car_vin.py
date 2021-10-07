# Generated by Django 3.2 on 2021-10-06 10:30

import Garage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0023_alter_car_vin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='vin',
            field=models.TextField(default=None, null=True, validators=[Garage.models.vin_validator], verbose_name='VIN-код'),
        ),
    ]
