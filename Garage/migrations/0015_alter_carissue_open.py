# Generated by Django 3.2 on 2021-08-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0014_alter_carissue_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carissue',
            name='open',
            field=models.BooleanField(default=True, verbose_name='Состояние'),
        ),
    ]
