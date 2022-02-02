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
        Car.objects.create(
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

    def test_for_logged_in_user_receives_insurances_that_are_not_archived(self):
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

        Insurance.objects.create(
            type='КАСКО архив',
            description='Test description',
            policy_number='ЕРО76ГО',
            start_date=date(2021, 12, 15),
            end_date=date(2022, 12, 14),
            price=34682,
            archive=True,
            car=car
        )

        response = c.get('/insurances/')
        self.assertEqual(response.status_code, 200)
        cars = response.context['cars']
        self.assertEqual(len(cars), 1)
        insurances = response.context['page_obj_insrncs']
        self.assertEqual(len(insurances.object_list), 2)


    def test_insurances_are_sent_to_archive_if_car_is_moved_to_archive(self):
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
            type='КАСКО ',
            description='Test description',
            policy_number='ЕРО76ГО',
            start_date=date(2021, 12, 15),
            end_date=date(2022, 12, 14),
            price=34682,
            car=car
        )
        response = c.get('/insurances/')
        insurances = response.context['page_obj_insrncs']
        self.assertEqual(len(insurances.object_list), 2)
        car.archive = True
        car.save()
        response = c.get('/insurances/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей и страховок')
