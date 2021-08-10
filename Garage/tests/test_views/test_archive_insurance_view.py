import datetime

from django.test import TestCase, Client
from Garage.models import Car, \
    Insurance, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestArchiveInsurance(TestCase):

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
            producer='Test Archive Insurance',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        Insurance.objects.create(
            type='Test Archive Insurance Type',
            description='Test Archive insurance Description',
            policy_number='RT 0000120',
            start_date=datetime.date(1999, 2, 4),
            end_date=datetime.date(2020, 2, 3),
            price=110,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        insrnc = Insurance.objects.get(type='Test Archive Insurance Type')
        response = c.get(f'/insurance/archive/{insrnc.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/insurance/archive/{insrnc.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_insurance_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/insurance/archive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_archive_insurance_view_for_logged_in_user(self):
        insrnc = Insurance.objects.get(type='Test Archive Insurance Type')
        c.login(username=username, password=password)
        response = c.get(f'/insurance/archive/{insrnc.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test Archive Insurance Type')
        response = c.get(f'/insurance/archive/{insrnc.id}')
        self.assertTemplateUsed(response, 'Garage/archive_insurance.html')

    def test_logged_in_user_sends_insurance_to_the_archive(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test Archive Insurance Type')
        car = Car.objects.get(producer='Test Archive Insurance')
        response = c.get(f'/insurance/archive/{insrnc.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/insurance/archive/{insrnc.id}')
        insrnc_re_requested = Insurance.objects.get(id=insrnc.id)
        self.assertTrue(insrnc_re_requested.archive)
        self.assertRedirects(r, f'/car/{car.id}', 302)
