import datetime

from django.test import TestCase, Client
from Garage.models import Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestArchiveCar(TestCase):

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

        Car.objects.create(
            producer='Test Archive Car',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )


    def test_not_logged_in_user_redirects_to_login_page(self):
        car = Car.objects.get(producer='Test Archive Car')
        response = c.get(f'/car/archive/{car.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/car/archive/{car.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_car_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/car/archive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_archive_car_view_for_logged_in_user(self):
        car = Car.objects.get(producer='Test Archive Car')
        c.login(username=username, password=password)
        response = c.get(f'/car/archive/{car.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        car = Car.objects.get(producer='Test Archive Car')
        response = c.get(f'/car/archive/{car.id}')
        self.assertTemplateUsed(response, 'Garage/archive_car.html')

    def test_logged_in_user_sends_car_and_all_related_objects_to_the_archive(self):
        c.login(username=username, password=password)
        car = Car.objects.get(producer='Test Archive Car')
        response = c.get(f'/car/archive/{car.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/car/archive/{car.id}')
        car_re_requested = Car.objects.get(producer='Test Archive Car')
        self.assertTrue(car_re_requested.archive)
        self.assertRedirects(r, '/cars/', 302)
