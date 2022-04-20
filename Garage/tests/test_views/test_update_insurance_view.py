import datetime

from django.test import TestCase, Client
from Garage.models import Insurance, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUpdateInsurance(TestCase):

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
            producer='Test Update Insurance',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        Insurance.objects.create(
            type='Test Update Type',
            description='Test Update Description',
            policy_number='AD 1063489',
            start_date=datetime.date(2019, 2, 4),
            end_date=datetime.date(2020, 2, 3),
            price=909.34,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        insrnc = Insurance.objects.get(type='Test Update Type')
        response = c.get(f'/insurance/update/{insrnc.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/insurance/update/{insrnc.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_insurance_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/insurance/update/2')
        self.assertEqual(response.status_code, 404)

    def test_render_update_insurance_view_for_logged_in_user(self):
        insrnc = Insurance.objects.get(type='Test Update Type')
        c.login(username=username, password=password)
        response = c.get(f'/insurance/update/{insrnc.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test Update Type')
        response = c.get(f'/insurance/update/{insrnc.id}')
        self.assertTemplateUsed(response, 'Garage/update_insurance.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test Update Type')
        response = c.get(f'/insurance/update/{insrnc.id}')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_updates_one_required_value_of_insurance_field(self):
        c.login(username=username, password=password)
        i = Insurance.objects.get(type='Test Update Type')
        car = Car.objects.get(producer='Test Update Insurance')
        response = c.get(f'/insurance/update/{i.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'type': 'Test new update type',
            'start_date': i.start_date,
            'end_date': i.end_date,
            'car': car.id
        }
        c.post(f'/insurance/update/{i.id}', data=data)
        insrnc = Insurance.objects.get(id=i.id)
        self.assertEqual(Insurance.objects.count(), 1)
        self.assertEqual(insrnc.type, 'Test new update type')
        self.assertEqual(insrnc.archive, False)
        self.assertEqual(insrnc.start_date, i.start_date)
        self.assertEqual(insrnc.end_date, i.end_date)
        self.assertEqual(insrnc.description, '')
        self.assertEqual(insrnc.policy_number, '')
        self.assertEqual(insrnc.car_id, i.car_id)

    def test_logged_in_user_updates_all_required_values_of_insurance_fields(self):
        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Select Second car for Update Insurance',
            model='Second car',
            year=2006,
            transmission=2,
            fuel=3,
            drive_system=1,
            user=user
        )
        c.login(username=username, password=password)
        i = Insurance.objects.get(type='Test Update Type')
        car = Car.objects.get(producer='Test Select Second car for Update Insurance')
        response = c.get(f'/insurance/update/{i.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'type': 'Test new update type',
            'start_date': datetime.date(2021, 2, 2),
            'end_date': datetime.date(2022, 2, 1),
            'car': car.id
        }
        c.post(f'/insurance/update/{i.id}', data=data)
        insrnc = Insurance.objects.get(id=i.id)
        self.assertEqual(Insurance.objects.count(), 1)
        self.assertEqual(insrnc.type, 'Test new update type')
        self.assertEqual(insrnc.start_date, datetime.date(2021, 2, 2))
        self.assertEqual(insrnc.end_date, datetime.date(2022, 2, 1))
        self.assertEqual(insrnc.archive, False)
        self.assertEqual(insrnc.car_id, car.id)
        self.assertEqual(insrnc.description, '')
        self.assertEqual(insrnc.policy_number, '')

    def test_logged_in_user_updates_all_values_of_insurance_fields(self):
        c.login(username=username, password=password)
        i = Insurance.objects.get(type='Test Update Type')
        car = Car.objects.get(producer='Test Update Insurance')
        response = c.get(f'/insurance/update/{i.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'type': 'Test new update type',
            'description': 'New description',
            'policy_number': 'New policy_number',
            'start_date': i.start_date,
            'end_date': i.end_date,
            'car': car.id
        }
        response = c.post(f'/insurance/update/{i.id}', data=data)
        insrnc = Insurance.objects.get(id=i.id)
        self.assertEqual(Insurance.objects.count(), 1)
        self.assertEqual(insrnc.type, 'Test new update type')
        self.assertEqual(insrnc.archive, False)
        self.assertEqual(insrnc.start_date, i.start_date)
        self.assertEqual(insrnc.end_date, i.end_date)
        self.assertEqual(insrnc.description, 'New description')
        self.assertEqual(insrnc.policy_number, 'New policy_number')
        self.assertEqual(insrnc.car_id, i.car_id)
        self.assertRedirects(response, f'/car/{car.id}', 302)

    def test_logged_in_user_receives_error_messages(self):
        user = User.objects.get(username=username)
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test Update Type')
        car = Car.objects.get(producer='Test Update Insurance', user_id=user.id)
        data = {
            'type': '',
            'start_date': datetime.date(2021, 2, 2),
            'end_date': datetime.date(2022, 2, 1),
            'car': car.id
        }
        response = c.post(f'/insurance/update/{insrnc.id}', data=data)
        self.assertTrue(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/update_insurance.html')
