from django.test import TestCase
from Garage.models import (
    Car,
    CarProblem,
    Body,
    Engine,
    Improvement,
    Insurance,
    Repair,
    User
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
            producer='Марка',
            model='Модель',
            year=2006,
            transmission='автомат',
            fuel=1,
            drive_system=1,
            user=user
        )

    def test_check_car_instance(self):
        car = Car.objects.get(id=1)
        self.assertTrue(isinstance(car, Car))

    def test_name_label(self):
        car = Car.objects.get(id=1)
        producer_label = car._meta.get_field('producer').verbose_name
        model_labl = car._meta.get_field('model').verbose_name
        self.assertEqual(car.__str__(), str(producer_label + ', ' + model_labl))

    def test_check_save_date_in_db(self):
        car = Car.objects.get(id=1)
        self.assertEqual(car.producer, 'Марка')
        self.assertEqual(car.model, 'Модель')
        self.assertEqual(car.year, 2006)
        self.assertEqual(car.transmission, 'автомат')
        self.assertEqual(car.fuel, 1)
        self.assertEqual(car.drive_system, 1)
        self.assertTrue(car.user_id)

    def test_add_optional_fields_of_model(self):
        Body.objects.get_or_create(name='Седан')
        body = Body.objects.get(name='Седан')
        Engine.objects.create(name='2.2')
        engine = Engine.objects.get(name='2.2')
        Car.objects.filter(id=1).update(
            mileage=20000,
            body=body.id,
            engine=engine.id,
            price=9300
        )
        car = Car.objects.get(id=1)
        self.assertEqual(car.mileage, 20000)
        self.assertTrue(car.body, 'Седан')
        self.assertTrue(car.engine, '2.2')
        self.assertTrue(car.price, 9300)
