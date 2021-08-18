import datetime

from django.contrib.messages import get_messages
from django.test import TestCase, Client

from Garage.models import User, \
    CarIssue, \
    Car

c = Client()
username = 'testuser'
password = '1234567890'

class TestDeleteIssue(TestCase):

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

        CarIssue.objects.create(
            name='Test delete issue',
            description='Test delete description',
            date=datetime.date(2020, 3, 14),
            open=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        issue = CarIssue.objects.get(name='Test delete issue')
        response = c.get(f'/issue/delete/{issue.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/issue/delete/{issue.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_issue_id_gets_404_error(self):
        c.login(username=username, password=password)
        response = c.get(f'/issue/delete/2')
        self.assertEqual(response.status_code, 404)

    def test_render_delete_issue_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test delete issue')
        response = c.get(f'/issue/delete/{issue.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test delete issue')
        response = c.get(f'/issue/delete/{issue.id}')
        self.assertTemplateUsed(response, 'Garage/delete_issue.html')

    def test_logged_in_user_successfully_deletes_issue(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test delete issue')
        self.assertEqual(CarIssue.objects.count(), 1)
        c.post(f'/issue/delete/{issue.id}')
        self.assertEqual(CarIssue.objects.count(), 0)

    def test_logged_in_user_receives_success_message_after_delete_issue(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test delete issue')
        self.assertEqual(CarIssue.objects.count(), 1)
        response = c.post(f"/issue/delete/{issue.id}")
        self.assertEqual(CarIssue.objects.count(), 0)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, 'Поломка была успешно удалена!')

    def test_redirect_for_logged_in_user_after_deleted_issue(self):
        c.login(username=username, password=password)
        issue = CarIssue.objects.get(name='Test delete issue')
        car = Car.objects.get(id=issue.car_id)
        response = c.post(f'/issue/delete/{issue.id}')
        self.assertRedirects(response, f'/car/{car.id}')
