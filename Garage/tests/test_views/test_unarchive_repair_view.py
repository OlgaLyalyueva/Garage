import datetime

from django.test import TestCase, Client
from Garage.models import Repair, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUnarchiveRepair(TestCase):

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
            producer='Test Unarchive Repair',
            model='car',
            year=1899,
            transmission='другое',
            fuel=1,
            drive_system=3,
            archive=True,
            user=user
        )

        Repair.objects.create(
            type_of_repair=2,
            name='замена лампочек',
            description='R5',
            note='Сергей Ефремов',
            mileage=129000,
            price=340.55,
            date=datetime.date.today(),
            archive=True,
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        repair = Repair.objects.get(name='замена лампочек')
        response = c.get(f'/repair/unarchive/{repair.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/repair/unarchive/{repair.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_repair_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/repair/unarchive/2')
        self.assertEqual(response.status_code, 404)

    def test_render_unarchive_repair_view_for_logged_in_user(self):
        repair = Repair.objects.get(name='замена лампочек')
        c.login(username=username, password=password)
        response = c.get(f'/repair/unarchive/{repair.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='замена лампочек')
        response = c.get(f'/repair/unarchive/{repair.id}')
        self.assertTemplateUsed(response, 'Garage/unarchive_repair.html')

    def test_logged_in_user_returns_repair_from_the_archive(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='замена лампочек')
        response = c.get(f'/repair/unarchive/{repair.id}')
        self.assertEqual(response.status_code, 200)
        r = c.post(f'/repair/unarchive/{repair.id}')
        repair_re_requested = Repair.objects.get(name='замена лампочек')
        self.assertFalse(repair_re_requested.archive)
        self.assertRedirects(r, f'/car/{repair.car_id}', 302)
