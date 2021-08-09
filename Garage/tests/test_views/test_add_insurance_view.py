import datetime
from django.test import TestCase, Client
from Garage.models import (
    Car,
    User,
    Insurance
)

c = Client()
link = '/insurance/add/'
username = 'testuser'
password = '1234567890'


class TestAddInsurance(TestCase):

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

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get(link)
        self.assertRedirects(response, '/accounts/login/?next=/insurance/add/', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_without_car_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 404)

    def test_render_insurance_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        response = c.get(link)
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        response = c.get(link)
        self.assertTemplateUsed(response, 'Garage/add_insurance.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)

        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        response = c.get(link)
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_creates_insurance_with_all_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'type': 'Test type',
            'description': 'test description',
            'policy_number': 'AR 5674326',
            'start_date': datetime.date(2020, 7, 1),
            'end_date': datetime.date(2021, 7, 2),
            'price': 245,
            'car': car.id
        }
        response = c.post("/insurance/add/", data=data)
        insrnc = Insurance.objects.get(type='Test type')
        self.assertEqual(Insurance.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(insrnc.type, 'Test type')
        self.assertEqual(insrnc.description, 'test description')
        self.assertEqual(insrnc.policy_number, 'AR 5674326')
        self.assertEqual(insrnc.start_date, datetime.date(2020, 7, 1))
        self.assertEqual(insrnc.end_date, datetime.date(2021, 7, 2))
        self.assertEqual(insrnc.price, 245)
        self.assertFalse(insrnc.archive)
        self.assertEqual(insrnc.car_id, car.id)

    def test_logged_in_user_creates_insurance_with_required_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'type': 'Test type',
            'start_date': datetime.date(2020, 7, 1),
            'end_date': datetime.date(2021, 7, 2),
            'car': car.id
        }
        response = c.post("/insurance/add/", data=data)
        insrnc = Insurance.objects.get(type='Test type')
        self.assertEqual(Insurance.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(insrnc.type, 'Test type')
        self.assertEqual(insrnc.description, '')
        self.assertEqual(insrnc.policy_number, '')
        self.assertEqual(insrnc.start_date, datetime.date(2020, 7, 1))
        self.assertEqual(insrnc.end_date, datetime.date(2021, 7, 2))
        self.assertEqual(insrnc.price, None)
        self.assertFalse(insrnc.archive)
        self.assertEqual(insrnc.car_id, car.id)

    def test_logged_in_user_receives_error_messages(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'type': 'Test type',
            'car': car.id
        }
        response = c.post("/insurance/add/", data=data)
        self.assertEqual(Insurance.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 2)
        self.assertTemplateUsed(response, 'Garage/add_insurance.html')
