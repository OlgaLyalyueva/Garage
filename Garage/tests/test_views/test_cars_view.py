from django.test import TestCase, Client

from Garage.models import (
    Body,
    User,
    Engine,
    Car
)


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

        Car.objects.create(
            producer='Test Mazda in Archive',
            model='X6',
            year=2017,
            transmission='автомат',
            fuel=5,
            drive_system=1,
            archive=True,
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

    def test_logged_in_user_receives_cars_that_are_not_in_archive(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        cars = response.context['cars']
        self.assertEqual(len(cars), 2)

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

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/cars/')
        self.assertRedirects(response, '/accounts/login/?next=/cars/', 302)
