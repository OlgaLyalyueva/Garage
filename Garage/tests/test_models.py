import datetime

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
            producer='Suzuki',
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

    def test_meta_label_name(self):
        car = Car.objects.get(id=1)
        meta_label_name = car._meta.verbose_name
        self.assertEqual(meta_label_name, 'Автомобиль')

    def test_get_verbose_labels(self):
        car = Car.objects.get(id=1)
        producer_label = car._meta.get_field('producer').verbose_name
        model_label = car._meta.get_field('model').verbose_name
        year_label = car._meta.get_field('year').verbose_name
        transmission_label = car._meta.get_field('transmission').verbose_name
        fuel_label = car._meta.get_field('fuel').verbose_name
        drive_system_label = car._meta.get_field('drive_system').verbose_name
        mileage_label = car._meta.get_field('mileage').verbose_name
        price_label = car._meta.get_field('price').verbose_name
        self.assertEqual(producer_label, 'Марка')
        self.assertEqual(model_label, 'Модель')
        self.assertEqual(year_label, 'Год')
        self.assertEqual(transmission_label, 'КПП')
        self.assertEqual(fuel_label, 'Топливо')
        self.assertEqual(drive_system_label, 'Тип привода')
        self.assertEqual(mileage_label, 'Пробег')
        self.assertEqual(price_label, 'Стоимость')

    def test_check_save_data_in_db(self):
        car = Car.objects.get(id=1)
        self.assertEqual(car.producer, 'Suzuki')
        self.assertEqual(car.model, 'Модель')
        self.assertEqual(car.year, 2006)
        self.assertEqual(car.transmission, 'автомат')
        self.assertEqual(car.fuel, 1)
        self.assertEqual(car.drive_system, 1)
        self.assertTrue(car.user_id)

    def test_check_max_length_for_producer(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field('producer').max_length
        self.assertEqual(max_length, 300)

    def test_check_max_length_for_model(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field('model').max_length
        self.assertEqual(max_length, 300)

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


class TestBody(TestCase):

    @classmethod
    def setUpTestData(cls):
        Body.objects.create(
            name='Купе'
        )

    def test_check_body_instance(self):
        body = Body.objects.get(name='Купе')
        self.assertTrue(isinstance(body, Body))

    def test_meta_label_name(self):
        body = Body.objects.get(id=1)
        name_label = body._meta.verbose_name
        self.assertEqual(name_label, 'Тип кузова')

    def test_get_verbose_labels(self):
        body = Body.objects.get(id=1)
        name_label = body._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Тип кузова')

    def test_check_save_data_in_db(self):
        body = Body.objects.get(id=1)
        self.assertEqual(body.name, 'Купе')

    def test_check_max_length_for_name(self):
        body = Body.objects.get(id=1)
        max_length = body._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class TestEngine(TestCase):
    @classmethod
    def setUpTestData(cls):
        Engine.objects.create(
            name='2.5'
        )

    def test_check_engine_instance(self):
        engine = Engine.objects.get(name='2.5')
        self.assertTrue(isinstance(engine, Engine))

    def test_meta_label_name(self):
        engine = Engine.objects.get(id=1)
        name_label = engine._meta.verbose_name
        self.assertEqual(name_label, 'Тип двигателя')

    def test_get_verbose_labels(self):
        engine = Engine.objects.get(id=1)
        name_label = engine._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Тип двигателя')

    def test_check_save_data_in_db(self):
        engine = Engine.objects.get(id=1)
        self.assertEqual(engine.name, '2.5')

    def test_check_max_length_for_name(self):
        engine = Engine.objects.get(id=1)
        max_length = engine._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)


class TestInsurance(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            password='1234567890wW',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
            email='test@test.test'
        )

        car = Car.objects.create(
            producer='Nissan',
            model='X-trail',
            year=2010,
            transmission='автомат',
            fuel=2,
            drive_system=1,
            user=user
        )

        Insurance.objects.create(
            type='ОСАГО',
            start_date=datetime.date(2021, 3, 1),
            end_date=datetime.date(2021, 2, 28),
            price=600,
            car=car
        )

    def test_check_insurance_instance(self):
        insurance = Insurance.objects.get(id=1)
        self.assertTrue(isinstance(insurance, Insurance))

    def test_meta_label_name(self):
        insurance = Insurance.objects.get(id=1)
        meta_label_name = insurance._meta.verbose_name
        self.assertEqual(meta_label_name, 'Страховка')

    def test_get_verbose_labels(self):
        insurance = Insurance.objects.get(id=1)
        type_label = insurance._meta.get_field('type').verbose_name
        description_label = insurance._meta.get_field('description').verbose_name
        policy_number_label = insurance._meta.get_field('policy_number').verbose_name
        start_date_label = insurance._meta.get_field('start_date').verbose_name
        end_date_label = insurance._meta.get_field('end_date').verbose_name
        price_label = insurance._meta.get_field('price').verbose_name
        self.assertEqual(type_label, 'Тип страховки')
        self.assertEqual(description_label, 'Описание')
        self.assertEqual(policy_number_label, 'Номер страховки')
        self.assertEqual(start_date_label, 'Дата начала')
        self.assertEqual(end_date_label, 'Дата окончания')
        self.assertEqual(price_label, 'Стоимость страховки')

    def test_check_save_data_in_db(self):
        insurance = Insurance.objects.get(id=1)
        self.assertEqual(insurance.type, 'ОСАГО')
        self.assertEqual(insurance.start_date, datetime.date(2021, 3, 1))
        self.assertEqual(insurance.end_date, datetime.date(2021, 2, 28))
        self.assertEqual(insurance.price, 600)
        self.assertTrue(insurance.car)

    def test_check_max_length_for_producer(self):
        insurance = Insurance.objects.get(id=1)
        max_length = insurance._meta.get_field('type').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_model(self):
        insurance = Insurance.objects.get(id=1)
        max_length = insurance._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    def test_add_optional_fields_of_model(self):
        Insurance.objects.filter(id=1).update(
            description='ОСАГО Тас Банк',
            policy_number='AC23056'
        )
        insurance = Insurance.objects.get(id=1)
        self.assertEqual(insurance.description, 'ОСАГО Тас Банк')
        self.assertEqual(insurance.policy_number, 'AC23056')
        self.assertTrue(insurance.type)


class TestCarProblem(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            password='1234567890wW',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
            email='test@test.test'
        )

        car = Car.objects.create(
            producer='Land Rower',
            model='Discovery Sport',
            year=2013,
            transmission='автомат',
            fuel=2,
            drive_system=2,
            user=user
        )

        CarProblem.objects.create(
            name='Шумит шаровая',
            car=car
        )

    def test_check_car_problem_instance(self):
        car_problem = CarProblem.objects.get(id=1)
        self.assertTrue(isinstance(car_problem, CarProblem))

    def test_meta_label_name(self):
        car_problem = CarProblem.objects.get(id=1)
        meta_label_name = car_problem._meta.verbose_name
        self.assertEqual(meta_label_name, 'Тип неполадки')

    def test_get_verbose_lables(self):
        car_problem = CarProblem.objects.get(id=1)
        name = car_problem._meta.get_field('name').verbose_name
        description = car_problem._meta.get_field('description').verbose_name
        state = car_problem._meta.get_field('state').verbose_name
        self.assertEqual(name, 'Название проблемы')
        self.assertEqual(description, 'Описание')
        self.assertEqual(state, 'Состояние')

    def test_check_save_data_in_db(self):
        car_problem = CarProblem.objects.get(id=1)
        self.assertEqual(car_problem.name, 'Шумит шаровая')
        self.assertTrue(car_problem.state)
        self.assertTrue(car_problem.date)
        self.assertTrue(car_problem.car)

    def test_check_max_length_for_name(self):
        car_problem = CarProblem.objects.get(id=1)
        max_length = car_problem._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_description(self):
        car_problem = CarProblem.objects.get(id=1)
        max_length = car_problem._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_add_optional_fields_of_model(self):
        CarProblem.objects.filter(id=1).update(
            description='Шумит справа',
        )
        car_problem = CarProblem.objects.get(id=1)
        self.assertEqual(car_problem.description, 'Шумит справа')
