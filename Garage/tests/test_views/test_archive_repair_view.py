import datetime

from django.test import TestCase, Client
from Garage.models import Car, \
    Repair, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestArchiveRepair(TestCase):

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
            producer='Test Archive Repair',
            model='First car',
            year=2021,
            transmission=3,
            fuel=3,
            drive_system=1,
            user=user
        )

        Repair.objects.create(
            type_of_repair=3,
            name='Test Archive Repair Name',
            date=datetime.date.today(),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        repair = Repair.objects.get(name='Test Archive Repair Name')
        response = c.get(f'/repair/archive/{repair.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/repair/archive/{repair.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_repair_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/repair/archive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_archive_repair_view_for_logged_in_user(self):
        repair = Repair.objects.get(name='Test Archive Repair Name')
        c.login(username=username, password=password)
        response = c.get(f'/repair/archive/{repair.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test Archive Repair Name')
        response = c.get(f'/repair/archive/{repair.id}')
        self.assertTemplateUsed(response, 'Garage/archive_repair.html')

    def test_logged_in_user_sends_repair_to_the_archive(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test Archive Repair Name')
        car = Car.objects.get(producer='Test Archive Repair')
        response = c.get(f'/repair/archive/{repair.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/repair/archive/{repair.id}')
        repair_re_requested = Repair.objects.get(id=repair.id)
        self.assertTrue(repair_re_requested.archive)
        self.assertRedirects(r, f'/car/{car.id}', 302)
