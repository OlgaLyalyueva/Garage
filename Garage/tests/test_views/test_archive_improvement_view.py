import datetime

from django.test import TestCase, Client
from Garage.models import Car, \
    Improvement, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestArchiveImprovement(TestCase):

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
            producer='Test Archive Improvement',
            model='First car',
            year=2021,
            transmission='типтроник',
            fuel=3,
            drive_system=1,
            user=user
        )

        Improvement.objects.create(
            name='Test Archive Improvement name',
            description='Test Archive improvement Description',
            price=3,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        impr = Improvement.objects.get(name='Test Archive Improvement name')
        response = c.get(f'/improvement/archive/{impr.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/improvement/archive/{impr.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_improvement_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/improvement/archive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_archive_improvement_view_for_logged_in_user(self):
        impr = Improvement.objects.get(name='Test Archive Improvement name')
        c.login(username=username, password=password)
        response = c.get(f'/improvement/archive/{impr.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Archive Improvement name')
        response = c.get(f'/improvement/archive/{impr.id}')
        self.assertTemplateUsed(response, 'Garage/archive_improvement.html')

    def test_logged_in_user_sends_improvement_to_the_archive(self):
        c.login(username=username, password=password)
        impr = Improvement.objects.get(name='Test Archive Improvement name')
        car = Car.objects.get(producer='Test Archive Improvement')
        response = c.get(f'/improvement/archive/{impr.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/improvement/archive/{impr.id}')
        impr_re_requested = Improvement.objects.get(id=impr.id)
        self.assertTrue(impr_re_requested.archive)
        self.assertRedirects(r, f'/car/{car.id}', 302)
