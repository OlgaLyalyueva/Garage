from django.test import TestCase, Client

from Garage.models import (
    User,
    Car
)

c = Client()
username = 'testuser'
password = '1234567890'

class TestCarsArchivedView(TestCase):

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
            archive=True,
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

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get('/cars/archived/')
        self.assertRedirects(response, f'/accounts/login/?next=/cars/archived/', 302)

    def test_login(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        response = c.get('/cars/archived/')
        self.assertEqual(response.context['user'].username, username)

    def test_render_cars_archived_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/cars/archived/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/cars/archived/')
        self.assertTemplateUsed(response, 'Garage/archived_cars.html')

    def test_logged_in_user_without_archived_car_get_message(self):
        c.login(username=username, password=password)
        response = c.get('/cars/archived/')
        self.assertEqual(response.context['message'], 'У вас нет автомобилей в папке архив')

    def test_logged_in_user_receives_archived_cars(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/cars/archived/')
        cars = response.context['page_obj_cars']
        self.assertEqual(len(cars), 2)

    def test_logged_in_user_receives_all_data_on_cars(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/cars/archived/')
        cars = response.context['page_obj_cars']
        self.assertEqual(len(cars), 2)
        self.assertEqual(cars[0].producer, 'Test Honda')
        self.assertEqual(cars[0].model, 'CRV')
        self.assertEqual(cars[0].year, 2000)
        self.assertEqual(cars[0].transmission, 'типтроник')
        self.assertEqual(cars[0].fuel, 1)
        self.assertEqual(cars[0].drive_system, 2)
        self.assertEqual(cars[0].body, None)
        self.assertEqual(cars[0].engine, None)
