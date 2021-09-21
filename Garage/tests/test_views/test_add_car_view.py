from django.test import TestCase

from Garage.models import User, Car, Body, Engine
from django.test import Client


class TestAddCar(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True,
            is_staff =True
        )
        user.set_password('1234567890')
        user.save()

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/car/add/')
        self.assertRedirects(response, '/accounts/login/?next=/car/add/', 302)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/add/')
        self.assertTemplateUsed(response, 'Garage/add_car.html')

    def test_logged_in_user_create_car_without_body_and_engine(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'CRV',
            'year': 2000,
            'transmission': 'типтроник',
            'fuel': 9,
            'drive_system': 2,
            'body': '',
            'engine': '',
            'user': user
        }
        response = c.post("/car/add/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        self.assertEqual(car.body_id, None)
        self.assertEqual(car.engine_id, None)
        self.assertRedirects(response, f'/car/{car.id}')

    def test_logged_in_user_create_car_with_body(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'Test body',
            'year': 1999,
            'transmission': 'автомат',
            'fuel': 2,
            'drive_system': 1,
            'body': 'test body name',
            'engine': '',
            'user': user
        }
        c.post("/car/add/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        body = Body.objects.get(name=data['body'])
        self.assertEqual(body.name, 'test body name')
        self.assertEqual(car.body_id, body.id)
        self.assertEqual(car.engine_id, None)

    def test_logged_in_user_create_car_with_engine(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'Test body',
            'year': 1999,
            'transmission': 'автомат',
            'fuel': 2,
            'drive_system': 1,
            'body': '',
            'engine': 'test engine name',
            'user': user
        }
        c.post("/car/add/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        engine = Engine.objects.get(name=data['engine'])
        self.assertEqual(engine.name, 'test engine name')
        self.assertEqual(car.engine_id, engine.id)

    def test_logged_in_user_receives_error_messages(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'user': user
        }
        response = c.post("/car/add/", data=data)
        self.assertEqual(Car.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 5)
