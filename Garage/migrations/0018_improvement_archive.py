# Generated by Django 3.2 on 2021-09-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0017_auto_20210908_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='improvement',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]