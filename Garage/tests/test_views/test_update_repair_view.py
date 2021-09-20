import datetime

from django.test import TestCase, Client
from Garage.models import Repair, \
    Car, \
    User

c = Client()
username = 'testuser'
password = '1234567890'


class TestUpdateRepair(TestCase):

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
            producer='Test Update Repair',
            model='First car',
            year=2021,
            transmission='робот',
            fuel=2,
            drive_system=1,
            user=user
        )

        Repair.objects.create(
            type_of_repair=3,
            name='Test Update Name',
            description='Test Update Description',
            date=datetime.date(2020, 10, 17),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        repair = Repair.objects.get(name='Test Update Name')
        response = c.get(f'/repair/update/{repair.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/repair/update/{repair.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_repair_id_receives_404_error(self):
        c.login(username=username, password=password)
        response = c.get('/repair/update/2')
        self.assertEqual(response.status_code, 404)

    def test_render_update_repair_view_for_logged_in_user(self):
        repair = Repair.objects.get(name='Test Update Name')
        c.login(username=username, password=password)
        response = c.get(f'/repair/update/{repair.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test Update Name')
        response = c.get(f'/repair/update/{repair.id}')
        self.assertTemplateUsed(response, 'Garage/update_repair.html')

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test Update Name')
        response = c.get(f'/repair/update/{repair.id}')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_logged_in_user_updates_required_value_of_repair_field(self):
        c.login(username=username, password=password)
        r = Repair.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Repair')
        response = c.get(f'/repair/update/{r.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'type_of_repair': 1,
            'name': 'Test new update name',
            'date': r.date,
            'car': car.id
        }
        c.post(f'/repair/update/{r.id}', data=data)
        repair = Repair.objects.get(id=r.id)
        self.assertEqual(Repair.objects.count(), 1)
        self.assertEqual(repair.type_of_repair, 1)
        self.assertEqual(repair.name, 'Test new update name')
        self.assertEqual(repair.description, None)
        self.assertEqual(repair.note, None)
        self.assertEqual(repair.mileage, None)
        self.assertEqual(repair.price, None)
        self.assertEqual(repair.date, r.date)
        self.assertEqual(repair.car_id, r.car_id)
        self.assertFalse(repair.archive)

    def test_logged_in_user_updates_all_values_of_repair_fields(self):
        c.login(username=username, password=password)
        r = Repair.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Repair')
        response = c.get(f'/repair/update/{r.id}')
        self.assertEqual(response.status_code, 200)
        data = {
            'type_of_repair': 1,
            'name': 'Test new update name',
            'description': 'New description',
            'note': 'test note',
            'mileage': 5079,
            'price': 12001.34,
            'date': datetime.date(2021, 3, 4),
            'car': car.id
        }
        response = c.post(f'/repair/update/{r.id}', data=data)
        repair = Repair.objects.get(id=r.id)
        self.assertEqual(Repair.objects.count(), 1)
        self.assertEqual(repair.type_of_repair, data['type_of_repair'])
        self.assertEqual(repair.name, data['name'])
        self.assertEqual(repair.description, data['description'])
        self.assertEqual(repair.note, data['note'])
        self.assertEqual(repair.mileage, data['mileage'])
        self.assertEqual(repair.price, data['price'])
        self.assertEqual(repair.date, data['date'])
        self.assertEqual(repair.car_id, r.car_id)
        self.assertFalse(repair.archive)
        self.assertRedirects(response, f'/car/{car.id}', 302)

    def test_logged_in_user_receives_error_messages(self):
        user = User.objects.get(username=username)
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test Update Name')
        car = Car.objects.get(producer='Test Update Repair', user_id=user.id, archive=False)
        data = {
            'name': '',
            'date': datetime.date(2021, 3, 4),
            'description': 'New description',
            'car': car.id
        }
        response = c.post(f'/repair/update/{repair.id}', data=data)
        self.assertTrue(len(response.context['errors']), 1)
        self.assertTemplateUsed(response, 'Garage/update_repair.html')
