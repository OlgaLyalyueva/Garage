import datetime

from django.test import TestCase, Client
from Garage.models import Car, \
    CarIssue, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestArchiveIssue(TestCase):

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
            producer='Test Archive Issue',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        CarIssue.objects.create(
            name='Test Archive Issue Name',
            description='Test Archive issue description',
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        issue = CarIssue.objects.get(name='Test Archive Issue Name')
        response = c.get(f'/issue/archive/{issue.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/issue/archive/{issue.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_issue_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/issue/archive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_archive_issue_view_for_logged_in_user(self):
        issue = CarIssue.objects.get(name='Test Archive Issue Name')
        c.login(username=username, password=password)
        response = c.get(f'/issue/archive/{issue.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test Archive Issue Name')
        response = c.get(f'/issue/archive/{issue.id}')
        self.assertTemplateUsed(response, 'Garage/archive_issue.html')

    def test_logged_in_user_sends_issue_to_the_archive(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test Archive Issue Name')
        car = Car.objects.get(producer='Test Archive Issue')
        response = c.get(f'/issue/archive/{issue.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/issue/archive/{issue.id}')
        issue_re_requested = CarIssue.objects.get(id=issue.id)
        self.assertTrue(issue_re_requested.archive)
        self.assertRedirects(r, f'/car/{car.id}', 302)
