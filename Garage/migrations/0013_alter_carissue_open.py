# Generated by Django 3.2 on 2021-08-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0012_rename_state_carissue_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carissue',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
