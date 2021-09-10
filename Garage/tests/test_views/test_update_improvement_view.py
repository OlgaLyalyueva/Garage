import datetime

from django.test import TestCase, Client
from Garage.models import Improvement, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUpdateImprovement(TestCase):

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
            producer='Test Update Improvement',
            model='First car',
            year=1990,
            transmission='газ пропан-бутан',
            fuel=1,
            drive_system=2,
            user=user
        )

        Improvement.objects.create(
            name='Test Update name',
            description='Test Update Description',
            price=10909.02,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        impr = Improvement.objects.get(name='Test Update name')
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/improvement/update/{impr.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_improvement_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/improvement/update/2')
        self.assertEqual(response.status_code, 404)

    def test_render_update_improvement_view_for_logged_in_user(self):
        impr = Improvement.objects.get(name='Test Update name')
        c.login(username=username, password=password)
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Update name')
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertTemplateUsed(response, 'Garage/update_improvement.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Update name')
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_updates_one_required_value_of_improvement_field(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Update name')
        car = Car.objects.get(producer='Test Update Improvement')
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Test new update name',
            'description': impr.description,
            'state': impr.state,
            'price': impr.price,
            'car': car.id
        }
        c.post(f'/improvement/update/{impr.id}', data=data)
        improvement = Improvement.objects.get(id=impr.id)
        self.assertEqual(Improvement.objects.count(), 1)
        self.assertEqual(improvement.name, 'Test new update name')
        self.assertEqual(improvement.description, impr.description)
        self.assertEqual(improvement.state, impr.state)
        self.assertEqual(improvement.price, impr.price)
        self.assertEqual(improvement.date, datetime.date.today())
        self.assertEqual(improvement.car_id, impr.car_id)
        self.assertFalse(improvement.archive)

    def test_logged_in_user_updates_all_values_of_improvement_fields(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Update name')
        car = Car.objects.get(producer='Test Update Improvement')
        response = c.get(f'/improvement/update/{impr.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Test new update name',
            'description': 'New description',
            'state': False,
            'price': 345,
            'car': car.id
        }
        response = c.post(f'/improvement/update/{impr.id}', data=data)
        improvement = Improvement.objects.get(id=impr.id)
        self.assertEqual(Improvement.objects.count(), 1)
        self.assertEqual(improvement.name, 'Test new update name')
        self.assertEqual(improvement.description, 'New description')
        self.assertFalse(improvement.state)
        self.assertEqual(improvement.price, 345)
        self.assertEqual(improvement.car_id, car.id)
        self.assertEqual(improvement.archive, False)
        self.assertRedirects(response, f'/car/{car.id}', 302)

    def test_logged_in_user_receives_error_messages(self):
        user = User.objects.get(username=username)
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Update name')
        car = Car.objects.get(producer='Test Update Improvement', user_id=user.id)
        data = {
            'name': '',
            'car': car.id
        }
        response = c.post(f'/improvement/update/{impr.id}', data=data)
        self.assertTrue(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/update_improvement.html')
