import datetime

from django.test import TestCase, Client
from Garage.models import Insurance, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUnarchiveInsurance(TestCase):

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
            producer='Test Unarchive Insurance',
            model='car',
            year=1899,
            transmission=9,
            fuel=1,
            drive_system=3,
            archive=True,
            user=user
        )

        Insurance.objects.create(
            type='ОСАГО',
            policy_number='R5FFD9',
            start_date=datetime.date(2021, 4, 16),
            end_date=datetime.date(2022, 4, 15),
            price=2310.56,
            archive=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        insrnc = Insurance.objects.get(type='ОСАГО')
        response = c.get(f'/insurance/unarchive/{insrnc.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/insurance/unarchive/{insrnc.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_insurance_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/insurance/unarchive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_unarchive_insurance_view_for_logged_in_user(self):
        insrnc = Insurance.objects.get(type='ОСАГО')
        c.login(username=username, password=password)
        response = c.get(f'/insurance/unarchive/{insrnc.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='ОСАГО')
        response = c.get(f'/insurance/unarchive/{insrnc.id}')
        self.assertTemplateUsed(response, 'Garage/unarchive_insurance.html')

    def test_logged_in_user_returns_insurance_from_the_archive(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='ОСАГО')
        response = c.get(f'/insurance/unarchive/{insrnc.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/insurance/unarchive/{insrnc.id}')
        insrnc_re_requested = Insurance.objects.get(type='ОСАГО')
        self.assertFalse(insrnc_re_requested.archive)
        self.assertRedirects(r, f'/car/{insrnc.car_id}', 302)
