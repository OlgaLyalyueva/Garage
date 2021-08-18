import datetime

from django.test import TestCase, Client
from Garage.models import CarIssue, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUpdateIssue(TestCase):

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
            producer='Test Update Issue',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        CarIssue.objects.create(
            name='Test Update Name',
            description='Test Update Description',
            open=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        issue = CarIssue.objects.get(name='Test Update Name')
        response = c.get(f'/issue/update/{issue.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/issue/update/{issue.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_issue_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/issue/update/2')
        self.assertEqual(response.status_code, 404)

    def test_render_update_issue_view_for_logged_in_user(self):
        issue = CarIssue.objects.get(name='Test Update Name')
        c.login(username=username, password=password)
        response = c.get(f'/issue/update/{issue.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test Update Name')
        response = c.get(f'/issue/update/{issue.id}')
        self.assertTemplateUsed(response, 'Garage/update_issue.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test Update Name')
        response = c.get(f'/issue/update/{issue.id}')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_updates_required_value_of_issue_field(self):
        c.login(username=username, password=password)
        i = CarIssue.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Issue')
        response = c.get(f'/issue/update/{i.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Test new update name',
            'date': i.date,
            'open': i.open,
            'car': car.id
        }
        c.post(f'/issue/update/{i.id}', data=data)
        issue = CarIssue.objects.get(id=i.id)
        self.assertEqual(CarIssue.objects.count(), 1)
        self.assertEqual(issue.name, 'Test new update name')
        self.assertEqual(issue.archive, False)
        self.assertEqual(issue.open, i.open)
        self.assertEqual(issue.date, i.date)
        self.assertEqual(issue.description, None)
        self.assertEqual(issue.car_id, i.car_id)

    def test_logged_in_user_updates_all_values_of_issue_fields(self):
        c.login(username=username, password=password)
        i = CarIssue.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Issue')
        response = c.get(f'/issue/update/{i.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Test new update name',
            'date': datetime.date(2021, 3, 4),
            'description': 'New description',
            'open': False,
            'car': car.id
        }
        response = c.post(f'/issue/update/{i.id}', data=data)
        issue = CarIssue.objects.get(id=i.id)
        self.assertEqual(CarIssue.objects.count(), 1)
        self.assertEqual(issue.name, 'Test new update name')
        self.assertEqual(issue.archive, False)
        self.assertEqual(issue.description, 'New description')
        self.assertEqual(issue.open, False)
        self.assertEqual(issue.car_id, i.car_id)
        self.assertEqual(issue.date, datetime.date(2021, 3, 4))
        self.assertRedirects(response, f'/car/{car.id}', 302)

    def test_logged_in_user_receives_error_messages(self):
        user = User.objects.get(username=username)
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Issue', user_id=user.id, archive=False)
        data = {
            'name': '',
            'date': datetime.date(2021, 3, 4),
            'description': 'New description',
            'open': False,
            'car': car.id
        }
        response = c.post(f'/issue/update/{issue.id}', data=data)
        self.assertTrue(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/update_issue.html')
