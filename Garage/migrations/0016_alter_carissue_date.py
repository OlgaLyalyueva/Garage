# Generated by Django 3.2 on 2021-08-17 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0015_alter_carissue_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carissue',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
