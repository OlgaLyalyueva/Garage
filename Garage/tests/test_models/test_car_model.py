from django.test import TestCase
from Garage.models import (
    Car,
    User,
    Body,
    Engine
)


class TestCarModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            password='1234567890wW',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
            email='test@test.test'
            )
        Car.objects.create(
            producer='Suzuki',
            model='Модель',
            year=2006,
            transmission=2,
            fuel=1,
            drive_system=1,
            user=user
        )

    def test_check_car_instance(self):
        car = Car.objects.get(producer='Suzuki')
        self.assertTrue(isinstance(car, Car))

    def test_meta_label_name(self):
        car = Car.objects.get(producer='Suzuki')
        meta_label_name = car._meta.verbose_name
        self.assertEqual(meta_label_name, 'Автомобиль')

    def test_get_verbose_labels(self):
        car = Car.objects.get(producer='Suzuki')
        producer_label = car._meta.get_field('producer').verbose_name
        model_label = car._meta.get_field('model').verbose_name
        vin_lable = car._meta.get_field('vin').verbose_name
        year_label = car._meta.get_field('year').verbose_name
        transmission_label = car._meta.get_field('transmission').verbose_name
        fuel_label = car._meta.get_field('fuel').verbose_name
        drive_system_label = car._meta.get_field('drive_system').verbose_name
        mileage_label = car._meta.get_field('mileage').verbose_name
        price_label = car._meta.get_field('price').verbose_name
        self.assertEqual(producer_label, 'Марка')
        self.assertEqual(model_label, 'Модель')
        self.assertEqual(vin_lable, 'VIN-код')
        self.assertEqual(year_label, 'Год')
        self.assertEqual(transmission_label, 'КПП')
        self.assertEqual(fuel_label, 'Топливо')
        self.assertEqual(drive_system_label, 'Тип привода')
        self.assertEqual(mileage_label, 'Пробег')
        self.assertEqual(price_label, 'Стоимость')

    def test_check_save_data_in_db(self):
        car = Car.objects.get(producer='Suzuki')
        self.assertEqual(car.producer, 'Suzuki')
        self.assertEqual(car.model, 'Модель')
        self.assertEqual(car.year, 2006)
        self.assertEqual(car.transmission, 2)
        self.assertEqual(car.fuel, 1)
        self.assertEqual(car.drive_system, 1)
        self.assertTrue(car.user_id)
        self.assertTrue(car.archive is False)

    def test_check_max_length_for_producer(self):
        car = Car.objects.get(producer='Suzuki')
        max_length = car._meta.get_field('producer').max_length
        self.assertEqual(max_length, 300)

    def test_check_max_length_for_model(self):
        car = Car.objects.get(producer='Suzuki')
        max_length = car._meta.get_field('model').max_length
        self.assertEqual(max_length, 300)

    def test_check_max_length_for_vin(self):
        car = Car.objects.get(producer='Suzuki')
        max_length = car._meta.get_field('vin').max_length
        self.assertEqual(max_length, 17)

    def test_add_optional_fields_of_model(self):
        Body.objects.get_or_create(name='Седан')
        body = Body.objects.get(name='Седан')
        Engine.objects.create(name='2.2')
        engine = Engine.objects.get(name='2.2')
        Car.objects.filter(producer='Suzuki').update(
            vin='ASE345VGRO4040012',
            mileage=20000,
            body=body.id,
            engine=engine.id,
            price=9300
        )
        car = Car.objects.get(producer='Suzuki')
        self.assertEqual(car.vin, 'ASE345VGRO4040012')
        self.assertEqual(car.mileage, 20000)
        self.assertTrue(car.body, 'Седан')
        self.assertTrue(car.engine, '2.2')
        self.assertTrue(car.price, 9300)
