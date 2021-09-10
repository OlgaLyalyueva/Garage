from django.contrib.messages import get_messages
from django.test import TestCase, Client

from Garage.models import User, \
    Improvement, \
    Car

c = Client()
username = 'testuser'
password = '1234567890'


class TestDeleteImprovement(TestCase):

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
            producer='Test delete improvement',
            model='Test delete model',
            year=2003,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )

        Improvement.objects.create(
            name='Test delete improvement',
            description='Test description',
            price=0,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        impr = Improvement.objects.get(name='Test delete improvement')
        response = c.get(f'/improvement/delete/{impr.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/improvement/delete/{impr.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_improvement_id_gets_404_error(self):
        c.login(username=username, password=password)
        response = c.get(f'/improvement/delete/2')
        self.assertEqual(response.status_code, 404)

    def test_render_delete_improvement_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test delete improvement')
        response = c.get(f'/improvement/delete/{impr.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test delete improvement')
        response = c.get(f'/improvement/delete/{impr.id}')
        self.assertTemplateUsed(response, 'Garage/delete_improvement.html')

    def test_logged_in_user_successfully_deletes_improvement(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test delete improvement')
        self.assertEqual(Improvement.objects.count(), 1)
        c.post(f'/improvement/delete/{impr.id}')
        self.assertEqual(Improvement.objects.count(), 0)

    def test_logged_in_user_receives_success_message_after_delete_improvement(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test delete improvement')
        self.assertEqual(Improvement.objects.count(), 1)
        response = c.post(f"/improvement/delete/{impr.id}")
        self.assertEqual(Improvement.objects.count(), 0)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, f'Улучшение {impr.name} было успешно удалено!')

    def test_redirect_for_logged_in_user_after_deleted_improvement(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test delete improvement')
        car = Car.objects.get(id=impr.car_id)
        response = c.post(f'/improvement/delete/{impr.id}')
        self.assertRedirects(response, f'/car/{car.id}')
