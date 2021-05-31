# Generated by Django 3.2 on 2021-04-21 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Garage', '0002_auto_20210419_0712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='body',
            options={'verbose_name': 'Тип кузова', 'verbose_name_plural': 'Типы кузовов'},
        ),
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.AlterModelOptions(
            name='carproblem',
            options={'verbose_name': 'Тип неполадки', 'verbose_name_plural': 'Типы неполадок'},
        ),
        migrations.AlterModelOptions(
            name='engine',
            options={'verbose_name': 'Двигатель', 'verbose_name_plural': 'Типы двигателей'},
        ),
        migrations.AlterModelOptions(
            name='improvement',
            options={'verbose_name': 'Улучшение', 'verbose_name_plural': 'Улучшения'},
        ),
        migrations.AlterModelOptions(
            name='insurance',
            options={'verbose_name': 'Страховка', 'verbose_name_plural': 'Страховки'},
        ),
        migrations.AlterModelOptions(
            name='repair',
            options={'verbose_name': 'Ремонт', 'verbose_name_plural': 'Ремонты'},
        ),
        migrations.AlterField(
            model_name='carproblem',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='improvement',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='description',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='note',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Примечание'),
        ),
    ]