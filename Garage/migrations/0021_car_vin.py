# Generated by Django 3.2 on 2021-10-06 10:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0020_repair_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='vin',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Код содержит 17 символов, убедитесь в этом!', regex='^\\w{17}$')]),
        ),
    ]
