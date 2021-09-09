import datetime
from django.test import TestCase, Client
from Garage.models import (
    Car,
    User,
    Improvement
)

c = Client()
link = '/improvement/add/'
username = 'testuser'
password = '1234567890'


class TestAddImprovement(TestCase):

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
        self.assertRedirects(response, '/accounts/login/?next=/improvement/add/', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_without_car_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 404)

    def test_render_improvement_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        response = c.get(link)
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        response = c.get(link)
        self.assertTemplateUsed(response, 'Garage/add_improvement.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)

        user = User.objects.get(username=username)

        Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        response = c.get(link)
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_creates_improvement_with_all_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        data = {
            'name': 'Test name',
            'description': 'test description',
            'price': 223.72,
            'car': car.id
        }
        response = c.post("/improvement/add/", data=data)
        improvement = Improvement.objects.get(name='Test name')
        self.assertEqual(Improvement.objects.count(), 1)
        self.assertEqual(Car.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(improvement.name, 'Test name')
        self.assertEqual(improvement.description, 'test description')
        self.assertEqual(improvement.price, 223.72)
        self.assertEqual(improvement.date, datetime.date.today())
        self.assertTrue(improvement.state)
        self.assertFalse(improvement.archive)
        self.assertEqual(improvement.car_id, car.id)

    def test_logged_in_user_creates_improvement_with_required_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        data = {
            'name': 'Test name',
            'car': car.id
        }
        response = c.post("/improvement/add/", data=data)
        improvement = Improvement.objects.get(name='Test name')
        self.assertEqual(Improvement.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(improvement.name, 'Test name')
        self.assertEqual(improvement.description, None)
        self.assertEqual(improvement.price, None)
        self.assertEqual(improvement.date, datetime.date.today())
        self.assertTrue(improvement.state)
        self.assertFalse(improvement.archive)
        self.assertEqual(improvement.car_id, car.id)

    def test_logged_in_user_receives_error_messages(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Improvement',
            model='First car',
            year=2000,
            transmission='автомат',
            fuel=1,
            drive_system=3,
            user=user
        )

        data = {
            'name': '',
            'car': car.id
        }
        response = c.post("/improvement/add/", data=data)
        self.assertEqual(Improvement.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/add_improvement.html')
