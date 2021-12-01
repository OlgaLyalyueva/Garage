# Generated by Django 3.2 on 2021-11-30 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0024_auto_20211130_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carphoto',
            name='title',
        ),
        migrations.AlterField(
            model_name='carphoto',
            name='car',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Garage.car'),
            preserve_default=False,
        ),
    ]
