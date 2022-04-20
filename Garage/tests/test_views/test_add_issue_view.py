import datetime

from django.test import TestCase, Client
from Garage.models import User, Car, CarIssue

c = Client()
link = '/issue/add/'
username = 'testuser'
password = '1234567890'

class TestAddIssue(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='testuser',
            is_active=True
        )

        user.set_password('1234567890')
        user.save()

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get(link)
        self.assertRedirects(response, '/accounts/login/?next=/issue/add/', 302)

    def test_logged_in(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_without_car_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 404)

    def test_render_issue_view_for_logged_in_user(self):
        user = User.objects.get(username=username)
        Car.objects.create(
            producer='Test Add Issue',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        user = User.objects.get(username=username)
        Car.objects.create(
            producer='Test Add Issue',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        c.login(username=username, password=password)
        response = c.get(link)
        self.assertTemplateUsed(response, 'Garage/add_issue.html')

    def test_logged_in_user_creates_issue_with_all_data(self):
        c.login(username=username, password=password)
        c.get(link)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Issue',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'name': 'Test name',
            'car': car.id,
            'description': 'Test Description'
        }
        response = c.post('/issue/add/', data=data)
        issue = CarIssue.objects.get(name='Test name')
        self.assertEqual(CarIssue.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(issue.name, 'Test name')
        self.assertEqual(issue.date, datetime.date.today())
        self.assertFalse(issue.close)
        self.assertEqual(issue.car_id, car.id)
        self.assertEqual(issue.description, 'Test Description')
        self.assertFalse(issue.archive)

    def test_logged_in_user_creates_issue_with_required_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Insurance',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'name': 'Test name',
            'car': car.id
        }
        response = c.post("/issue/add/", data=data)
        issue = CarIssue.objects.get(name='Test name')
        self.assertEqual(CarIssue.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(issue.name, 'Test name')
        self.assertEqual(issue.date, datetime.date.today())
        self.assertEqual(issue.close, False)
        self.assertEqual(issue.car_id, car.id)
        self.assertEqual(issue.description, None)

    def test_logged_in_user_receives_error_messages(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Issue',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        data = {
            'name': '',
            'car': car.id,
        }
        response = c.post("/issue/add/", data=data)
        self.assertEqual(CarIssue.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/add_issue.html')
