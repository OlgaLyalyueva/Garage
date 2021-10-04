from django.test import TestCase, Client
from Garage.models import Improvement, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUnarchiveImprovement(TestCase):

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
            producer='Test Unarchive Improvement',
            model='car',
            year=2019,
            transmission='другое',
            fuel=1,
            drive_system=3,
            archive=True,
            user=user
        )

        Improvement.objects.create(
            name='Замена заднего дворника',
            description='Bosh',
            price=1003,
            archive=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        impr = Improvement.objects.get(name='Замена заднего дворника')
        response = c.get(f'/improvement/unarchive/{impr.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/improvement/unarchive/{impr.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_improvement_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/improvement/unarchive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_unarchive_improvement_view_for_logged_in_user(self):
        impr = Improvement.objects.get(name='Замена заднего дворника')
        c.login(username=username, password=password)
        response = c.get(f'/improvement/unarchive/{impr.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Замена заднего дворника')
        response = c.get(f'/improvement/unarchive/{impr.id}')
        self.assertTemplateUsed(response, 'Garage/unarchive_improvement.html')

    def test_logged_in_user_returns_improvement_from_the_archive(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Замена заднего дворника')
        response = c.get(f'/improvement/unarchive/{impr.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/improvement/unarchive/{impr.id}')
        impr_re_requested = Improvement.objects.get(name='Замена заднего дворника')
        self.assertFalse(impr_re_requested.archive)
        self.assertRedirects(r, f'/car/{impr.car_id}', 302)
