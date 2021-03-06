# Generated by Django 3.2 on 2021-04-15 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Тип кузова')),
            ],
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=500, verbose_name='Тип двигателя')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('producer', models.CharField(max_length=300, verbose_name='Марка')),
                ('model', models.CharField(max_length=300, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('transmission', models.CharField(choices=[('ручная/механика', 'Ручная/Механика'), ('автомат', 'Автомат'), ('типтроник', 'Типтроник'), ('робот', 'Робот'), ('вариатор', 'Вариатор')], max_length=20, verbose_name='КПП')),
                ('fuel', models.PositiveIntegerField(choices=[(1, 'Бензин'), (2, 'Дизель'), (3, 'Газ'), (4, 'Газ/Бензин'), (5, 'Гибрид'), (6, 'Электро'), (7, 'Газ метан'), (8, 'Газ пропан-бутан'), (9, 'Другое')], verbose_name='Топливо')),
                ('drive_system', models.PositiveSmallIntegerField(choices=[(1, 'Полный'), (2, 'Передний'), (3, 'Задний')], verbose_name='Тип привода')),
                ('mileage', models.IntegerField(blank=True, null=True, verbose_name='Пробег')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Garage.body')),
                ('engine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Garage.engine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]
