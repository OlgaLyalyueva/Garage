from django.test import TestCase

from Garage.models import User, Car, Body
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

    def test_logged_in_user_update_year_and_body(self):
        c = Client()
        car_id = 1
        c.login(username='testuser', password='1234567890')
        response = c.get(f'/car/update/{car_id}')
        self.assertEqual(response.status_code, 200)
        car = Car.objects.get(id=car_id)
        body = Body.objects.get(name='Test body name')
        year = 2001
        form_car = CarForm(instance=car, data={'producer': car.producer, 'model': car.model, 'year': year, 'transmission': car.transmission, 'fuel': car.fuel, 'drive_system': car.drive_system})
        car.body_id = body.id
        self.assertTrue(form_car.is_valid())
        form_car.save()
        self.assertEqual(car.producer, 'Test update producer')
        self.assertEqual(car.model, 'Test update model')
        self.assertEqual(car.year, year)
        self.assertEqual(car.body_id, 1)
