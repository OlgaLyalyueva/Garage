import datetime

from django.contrib.messages import get_messages
from django.test import TestCase, Client

from Garage.models import User, \
    Insurance, \
    Car

c = Client()
username = 'testuser'
password = '1234567890'

class TestDeleteInsurance(TestCase):

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

        car = Car.objects.create(
            producer='Test delete producer',
            model='Test delete model',
            year=1990,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )

        Insurance.objects.create(
            type='Test delete insurance',
            description='Test description',
            policy_number='RE 3478901',
            start_date=datetime.date(2020, 3, 14),
            end_date=datetime.date(2021, 3, 13),
            price=345,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        insrnc = Insurance.objects.get(type='Test delete insurance')
        response = c.get(f'/insurance/delete/{insrnc.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/insurance/delete/{insrnc.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_insurance_id_gets_404_error(self):
        c.login(username=username, password=password)
        response = c.get(f'/insurance/delete/2')
        self.assertEqual(response.status_code, 404)

    def test_render_delete_insurance_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test delete insurance')
        response = c.get(f'/insurance/delete/{insrnc.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test delete insurance')
        response = c.get(f'/insurance/delete/{insrnc.id}')
        self.assertTemplateUsed(response, 'Garage/delete_insurance.html')

    def test_logged_in_user_successfully_deletes_insurance(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test delete insurance')
        self.assertEqual(Insurance.objects.count(), 1)
        c.post(f'/insurance/delete/{insrnc.id}')
        self.assertEqual(Insurance.objects.count(), 0)

    def test_logged_in_user_receives_success_message_after_delete_insurance(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test delete insurance')
        self.assertEqual(Insurance.objects.count(), 1)
        response = c.post(f"/insurance/delete/{insrnc.id}")
        self.assertEqual(Insurance.objects.count(), 0)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, f'Страховой полис {insrnc.type} №{insrnc.policy_number}, был успешно удален!')

    def test_redirect_for_logged_in_user_after_deleted_insurance(self):
        c.login(username=username, password=password)
        insrnc = Insurance.objects.get(type='Test delete insurance')
        car = Car.objects.get(id=insrnc.car_id)
        response = c.post(f'/insurance/delete/{insrnc.id}')
        self.assertRedirects(response, f'/car/{car.id}')
