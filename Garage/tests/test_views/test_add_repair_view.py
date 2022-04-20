import datetime

from django.test import TestCase, Client
from Garage.models import User, Car, Repair

c = Client()
link = '/repair/add/'
username = 'testuser'
password = '1234567890'

class TestAddRepair(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='testuser',
            is_active=True
        )

        user.set_password('1234567890')
        user.save()

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get(link)
        self.assertRedirects(response, '/accounts/login/?next=/repair/add/', 302)

    def test_logged_in(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_without_car_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 404)

    def test_render_repair_view_for_logged_in_user(self):
        user = User.objects.get(username=username)
        Car.objects.create(
            producer='Test Add Repair',
            model='First car',
            year=1845,
            transmission=1,
            fuel=1,
            drive_system=1,
            user=user
        )

        c.login(username=username, password=password)
        response = c.get(link)
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        user = User.objects.get(username=username)
        Car.objects.create(
            producer='Test Add Repair',
            model='First car',
            year=1845,
            transmission=1,
            fuel=1,
            drive_system=1,
            user=user
        )

        c.login(username=username, password=password)
        response = c.get(link)
        self.assertTemplateUsed(response, 'Garage/add_repair.html')

    def test_logged_in_user_creates_repair_with_all_data(self):
        c.login(username=username, password=password)
        c.get(link)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Repair',
            model='First car',
            year=1845,
            transmission=1,
            fuel=1,
            drive_system=1,
            user=user
        )

        data = {
            'type_of_repair': 1,
            'name': 'Name of repair',
            'description': 'Test Description',
            'note': 'Test note',
            'mileage': 123000,
            'date': datetime.date(2017, 1, 31),
            'price': 123.47,
            'car': car.id
        }
        response = c.post('/repair/add/', data=data)
        repair = Repair.objects.get(name='Name of repair')
        self.assertEqual(Repair.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(repair.type_of_repair, 1)
        self.assertEqual(repair.name, 'Name of repair')
        self.assertEqual(repair.description, 'Test Description')
        self.assertEqual(repair.mileage, 123000)
        self.assertEqual(repair.date, datetime.date(2017, 1, 31))
        self.assertEqual(repair.price, 123.47)
        self.assertEqual(repair.car_id, car.id)
        self.assertFalse(repair.archive)

    def test_logged_in_user_creates_repair_with_required_data(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Repair',
            model='First car',
            year=1845,
            transmission=1,
            fuel=1,
            drive_system=1,
            user=user
        )

        data = {
            'type_of_repair': 1,
            'name': 'Замена сажевого фильтра',
            'date': datetime.date.today(),
            'car': car.id
        }
        response = c.post("/repair/add/", data=data)
        repair = Repair.objects.get(name='Замена сажевого фильтра')
        self.assertEqual(Repair.objects.count(), 1)
        self.assertRedirects(response, f'/car/{car.id}')
        self.assertEqual(repair.type_of_repair, 1)
        self.assertEqual(repair.name, 'Замена сажевого фильтра')
        self.assertEqual(repair.description, None)
        self.assertEqual(repair.note, None)
        self.assertEqual(repair.mileage, None)
        self.assertEqual(repair.price, None)
        self.assertEqual(repair.date, datetime.date.today())
        self.assertEqual(repair.car_id, car.id)
        self.assertFalse(repair.archive)

    def test_logged_in_user_receives_error_messages(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)

        car = Car.objects.create(
            producer='Test Add Repair',
            model='First car',
            year=1845,
            transmission=1,
            fuel=1,
            drive_system=1,
            user=user
        )

        data = {
            'name': '',
            'car': car.id
        }
        response = c.post("/repair/add/", data=data)
        self.assertEqual(Repair.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 2)
        self.assertTemplateUsed(response, 'Garage/add_repair.html')
