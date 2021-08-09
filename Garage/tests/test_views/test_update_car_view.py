from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from Garage.models import User, Car, Body, Engine
from django.test import Client
from Garage.forms import CarForm


class TestUpdateCar(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True,
            is_staff=True
        )
        user.set_password('1234567890')
        user.save()

        Car.objects.create(
            producer='Test update producer',
            model='Test update model',
            year=1999,
            transmission='типтроник',
            fuel=9,
            drive_system=2,
            user=user
        )

        Body.objects.create(
            name='Test body name'
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/car/update/1')
        self.assertRedirects(response, '/accounts/login/?next=/car/update/1', 302)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/update/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Garage/update_car.html')

    def test_logged_in_user_updates_all_required_fields(self):
        c = Client()
        car_id = 1
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(id=car_id)
        user = User.objects.get(id=car.user_id)
        response = c.get(f'/car/update/{car_id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'producer': 'New producer',
            'model': 'New model',
            'year': 1999,
            'transmission': 'автомат',
            'fuel': 2,
            'drive_system': 3,
            'body': '',
            'engine': '',
            'user_id': user
        }
        c.post(f'/car/update/{car.id}', data=data)
        self.assertEqual(Car.objects.count(), 1)
        update_car = Car.objects.get(id=car_id)
        self.assertEqual(update_car.producer, 'New producer')
        self.assertEqual(update_car.model, 'New model')
        self.assertEqual(update_car.year, 1999)
        self.assertEqual(update_car.transmission, 'автомат')
        self.assertEqual(update_car.fuel, 2)
        self.assertEqual(update_car.drive_system, 3)
        self.assertEqual(update_car.mileage, None)
        self.assertEqual(update_car.price, None)
        self.assertEqual(update_car.body_id, None)
        self.assertEqual(update_car.engine_id, None)
        self.assertEqual(update_car.user_id, user.id)
        self.assertEqual(update_car.archive, False)

    def test_logged_in_user_updates_all_not_required_fields(self):
        c = Client()
        car_id = 1
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(id=car_id)
        user = User.objects.get(id=car.user_id)
        response = c.get(f'/car/update/{car_id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'producer': car.producer,
            'model': car.model,
            'year': car.year,
            'transmission': car.transmission,
            'fuel': car.fuel,
            'drive_system': car.drive_system,
            'mileage': 123000,
            'price': 23000,
            'body': 'body',
            'engine': 'engine',
            'user_id': user
        }
        response = c.post(f'/car/update/{car.id}', data=data)
        self.assertEqual(Car.objects.count(), 1)
        update_car = Car.objects.get(id=car_id)
        body = Body.objects.get(name='body')
        engine = Engine.objects.get(name='engine')
        self.assertEqual(update_car.producer, car.producer)
        self.assertEqual(update_car.model, car.model)
        self.assertEqual(update_car.year, car.year)
        self.assertEqual(update_car.transmission, car.transmission)
        self.assertEqual(update_car.fuel, car.fuel)
        self.assertEqual(update_car.drive_system, car.drive_system)
        self.assertEqual(update_car.mileage, 123000)
        self.assertEqual(update_car.price, 23000)
        self.assertEqual(update_car.body_id, body.id)
        self.assertEqual(update_car.engine_id, engine.id)
        self.assertEqual(update_car.user_id, user.id)
        self.assertEqual(update_car.archive, False)
        self.assertRedirects(response, f'/car/{car.id}', 302)

    def test_logged_in_user_receives_error_messages(self):
        c = Client()
        car_id = 1
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(id=car_id)
        user = User.objects.get(id=car.user_id)
        response = c.get(f'/car/update/{car_id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'price': 23000,
            'body': 'body',
            'engine': 'engine',
            'user_id': user
        }
        response = c.post(f'/car/update/{car.id}', data=data)
        self.assertEqual(len(response.context['errors']), 6)
        self.assertTemplateUsed(response, 'Garage/update_car.html')
