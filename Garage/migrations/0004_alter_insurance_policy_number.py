# Generated by Django 3.2 on 2021-04-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0003_auto_20210421_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='policy_number',
            field=models.CharField(blank=True, max_length=30, verbose_name='Номер страховки'),
        ),
    ]