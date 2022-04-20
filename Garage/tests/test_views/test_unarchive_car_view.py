from django.test import TestCase, Client
from Garage.models import Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUnarchiveCar(TestCase):

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
            producer='Test Unarchive Car',
            model='car',
            year=2003,
            transmission=9,
            fuel=6,
            drive_system=2,
            archive=True,
            user=user
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        car = Car.objects.get(producer='Test Unarchive Car')
        response = c.get(f'/car/unarchive/{car.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/car/unarchive/{car.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_car_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/car/unarchive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_unarchive_car_view_for_logged_in_user(self):
        car = Car.objects.get(producer='Test Unarchive Car')
        c.login(username=username, password=password)
        response = c.get(f'/car/unarchive/{car.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        car = Car.objects.get(producer='Test Unarchive Car')
        response = c.get(f'/car/unarchive/{car.id}')
        self.assertTemplateUsed(response, 'Garage/unarchive_car.html')

    def test_logged_in_user_returns_car_from_the_archive(self):
        c.login(username=username, password=password)
        car = Car.objects.get(producer='Test Unarchive Car')
        response = c.get(f'/car/unarchive/{car.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/car/unarchive/{car.id}')
        car_re_requested = Car.objects.get(producer='Test Unarchive Car')
        self.assertFalse(car_re_requested.archive)
        self.assertRedirects(r, f'/car/{car.id}', 302)
