from django.test import TestCase
from Garage.models import User, Car, Body, Engine, CarProblem, Improvement, Insurance, Repair
from django.test import Client
from datetime import date


class TestCarsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        first_user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True
        )
        first_user.set_password('1234567890')
        first_user.save()

        second_user = User.objects.create_user(
            username='second-testuser',
            first_name='Test 2',
            last_name='T 2',
            email='test+2@test.test',
            is_active=True
        )
        second_user.set_password('1234567890')
        second_user.save()

        body = Body.objects.create(
            name='Test body name'
        )

        engine = Engine.objects.create(
            name='Test engine name'
        )

        Car.objects.create(
            producer='Test Tesla',
            model='X',
            year=2019,
            transmission='автомат',
            fuel=6,
            drive_system=2,
            user=second_user
        )

        Car.objects.create(
            producer='Test Honda',
            model='CRV',
            year=2000,
            transmission='типтроник',
            fuel=1,
            drive_system=2,
            body_id=body.id,
            engine_id=engine.id,
            user=second_user
        )

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_render_cars_view_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_without_car_get_message(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей')


    def test_logged_in_user_receives_all_data_on_cars(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        cars = response.context['cars']
        self.assertEqual(len(cars), 2)
        self.assertEqual(cars[0].producer, 'Test Tesla')
        self.assertEqual(cars[0].model, 'X')
        self.assertEqual(cars[0].year, 2019)
        self.assertEqual(cars[0].transmission, 'автомат')
        self.assertEqual(cars[0].fuel, 6)
        self.assertEqual(cars[0].drive_system, 2)
        self.assertEqual(cars[0].body, None)
        self.assertEqual(cars[0].engine, None)

    def test_logged_in_user_receives_name_of_car_body(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['body_name'], 'Test body name')

    def test_logged_in_user_receives_name_of_car_engine(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['engine_name'], 'Test engine name')

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/cars/')
        self.assertRedirects(response, '/accounts/login/', 302)


class TestCarView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True
        )
        user.set_password('1234567890')
        user.save()

        car = Car.objects.create(
            producer='Test Car with insurance, improvement, repair, car problems',
            model='X car',
            year=1999,
            transmission='автомат',
            fuel=5,
            drive_system=2,
            user=user
        )

        Car.objects.create(
            producer='Test car',
            model='CRV',
            year=2000,
            transmission='типтроник',
            fuel=9,
            drive_system=2,
            user=user
        )

        CarProblem.objects.create(
            name='Test car problem',
            description='Test description',
            state=False,
            date=date.today(),
            car_id=car.id
        )

        Insurance.objects.create(
            type='Test ОСАГО',
            policy_number='AP456789',
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
            price=599.43,
            car_id=car.id
        )

        Improvement.objects.create(
            name='Test name',
            car_id=car.id
        )

        Repair.objects.create(
            type_of_repair=1,
            name='Замена масла в коробке',
            description='ATF SP-III',
            mileage=80000,
            price=1500.05,
            date=date.today(),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get(f'/car/1')
        self.assertRedirects(response, '/accounts/login/', 302)

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_render_car_view_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(response.status_code, 200)
