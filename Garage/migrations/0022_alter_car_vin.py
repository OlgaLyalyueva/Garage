# Generated by Django 3.2 on 2021-10-07 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0021_car_vin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='vin',
            field=models.CharField(blank=True, max_length=17, null=True, verbose_name='VIN-код'),
        ),
    ]
