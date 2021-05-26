from django.test import TestCase

from Garage.models import User, Car, Insurance
from django.test import Client
from datetime import date


class TestInsurances(TestCase):

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

    def test_not_logged_in_user_redirect_to_login_page(self):
        c = Client()
        response = c.get('/insurances/')
        self.assertRedirects(response, '/accounts/login/?next=/insurances/', 302)

    def test_view_exists_for_logged_in_user_without_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/insurances/')
        self.assertEqual(response.status_code, 200)

    def test_view_exists_for_logged_in_user_without_insurance(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        car1 = Car.objects.create(
            producer='Test insurance producer',
            model='Test insurance model',
            year=1990,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )

        response = c.get('/insurances/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/insurances/')
        self.assertTemplateUsed(response, 'Garage/insurances.html')

    def test_for_logged_in_user_with_insurances(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')

        car = Car.objects.create(
            producer='Test insurance producer',
            model='Test insurance model',
            year=1990,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )

        Car.objects.create(
            producer='Test insurance 2 producer',
            model='Test insurance model',
            year=1990,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )
        Insurance.objects.create(
            type='ОСАГО',
            description='Test description',
            policy_number='AT23RT1',
            start_date=date(2021, 1, 3),
            end_date=date(2022, 1, 2),
            price=2300.78,
            car=car
        )

        Insurance.objects.create(
            type='КАСКО',
            description='Test description',
            policy_number='ЕРО76ГО',
            start_date=date(2021, 12, 15),
            end_date=date(2022, 12, 14),
            price=34682,
            car=car
        )

        response = c.get('/insurances/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Insurance.objects.count(), 2)
