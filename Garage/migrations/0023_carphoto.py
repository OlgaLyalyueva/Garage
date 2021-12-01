# Generated by Django 3.2 on 2021-11-30 07:12

import Garage.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0022_alter_car_vin'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=Garage.models.user_directory_path)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Garage.car')),
            ],
        ),
    ]
