from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    producer = models.CharField(max_length=300, verbose_name='Марка')
    model = models.CharField(max_length=300, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год')
    transmission = models.CharField(choices=[
        ('ручная/механика', 'Ручная/Механика'),
        ('автомат', 'Автомат'),
        ('типтроник', 'Типтроник'),
        ('робот', 'Робот'),
        ('вариатор', 'Вариатор')
    ], max_length=20, verbose_name='КПП')
    body = models.ForeignKey('Body', on_delete=models.CASCADE, null=True)
    engine = models.ForeignKey('Engine', on_delete=models.CASCADE, null=True)
    fuel = models.PositiveIntegerField(choices=[
        (1, 'Бензин'),
        (2, 'Дизель'),
        (3, 'Газ'),
        (4, 'Газ/Бензин'),
        (5, 'Гибрид'),
        (6, 'Электро'),
        (7, 'Газ метан'),
        (8, 'Газ пропан-бутан'),
        (9, 'Другое')
    ], verbose_name='Топливо')
    drive_system = models.PositiveSmallIntegerField(choices=[
        (1, 'Полный'),
        (2, 'Передний'),
        (3, 'Задний')
    ], verbose_name='Тип привода')
    mileage = models.IntegerField(blank=True, null=True, verbose_name='Пробег')
    price = models.FloatField(blank=True, null=True, verbose_name='Стоимость')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.producer + ', ' + self.model

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Body(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(blank=True, max_length=100, verbose_name='Тип кузова')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузовов'


class Engine(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(blank=True, max_length=500, verbose_name='Тип двигателя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип двигателя'
        verbose_name_plural = 'Типы двигателей'


class Insurance(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    type = models.CharField(max_length=255, verbose_name='Тип страховки')
    description = models.CharField(blank=True, max_length=500, verbose_name='Описание')
    policy_number = models.CharField(blank=True, max_length=30, verbose_name='Номер страховки')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    price = models.FloatField(verbose_name='Стоимость страховки')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Страховка'
        verbose_name_plural = 'Страховки'


class CarIssue(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    date = models.DateField(auto_now=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Название проблемы')
    description = models.CharField(blank=True, null=True, max_length=1000, verbose_name='Описание')
    state = models.BooleanField(default=True, verbose_name='Состояние')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип неполадки'
        verbose_name_plural = 'Типы неполадок'


class Improvement(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    date = models.DateField(auto_now=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Название проблемы')
    description = models.CharField(blank=True, null=True, max_length=1000, verbose_name='Описание')
    state = models.BooleanField(default=True, verbose_name='Состояние')
    price = models.FloatField(blank=True, null=True, verbose_name='Стоимость')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Улучшение'
        verbose_name_plural = 'Улучшения'


class Repair(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    type_of_repair = models.PositiveSmallIntegerField(choices=[
        (1, 'ТО'),
        (2, 'Замена запчастей'),
        (3, 'Кузовные работы')
    ])
    name = models.CharField(max_length=400, verbose_name='Название')
    description = models.CharField(blank=True, null=True, max_length=2000, verbose_name='Описание')
    note = models.CharField(blank=True, null=True, max_length=500, verbose_name='Примечание')
    mileage = models.IntegerField(blank=True, null=True, verbose_name='Пробег')
    price = models.FloatField(blank=True, null=True, verbose_name='Стоимость')
    date = models.DateField(blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ремонт'
        verbose_name_plural = 'Ремонты'
