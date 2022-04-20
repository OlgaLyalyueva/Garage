from django.test import TestCase, Client
from Garage.models import CarIssue, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUnarchiveIssue(TestCase):

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
            producer='Test Unarchive Issue',
            model='car',
            year=2016,
            transmission=3,
            fuel=1,
            drive_system=3,
            user=user
        )

        CarIssue.objects.create(
            name='Замена сайлентблоков',
            description='машину ведет в правую сторону',
            archive=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        issue = CarIssue.objects.get(name='Замена сайлентблоков')
        response = c.get(f'/issue/unarchive/{issue.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/issue/unarchive/{issue.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_issue_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/issue/unarchive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_unarchive_issue_view_for_logged_in_user(self):
        issue = CarIssue.objects.get(name='Замена сайлентблоков')
        c.login(username=username, password=password)
        response = c.get(f'/issue/unarchive/{issue.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Замена сайлентблоков')
        response = c.get(f'/issue/unarchive/{issue.id}')
        self.assertTemplateUsed(response, 'Garage/unarchive_issue.html')

    def test_logged_in_user_returns_issue_from_the_archive(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Замена сайлентблоков')
        response = c.get(f'/issue/unarchive/{issue.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/issue/unarchive/{issue.id}')
        issue_re_requested = CarIssue.objects.get(name='Замена сайлентблоков')
        self.assertFalse(issue_re_requested.archive)
        self.assertRedirects(r, f'/car/{issue.car_id}', 302)
