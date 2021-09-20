import datetime

from django.contrib.messages import get_messages
from django.test import TestCase, Client

from Garage.models import User, \
    Repair, \
    Car

c = Client()
username = 'testuser'
password = '1234567890'

class TestDeleteRepair(TestCase):

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

        Repair.objects.create(
            type_of_repair=2,
            name='Test delete repair',
            date=datetime.date(2020, 3, 14),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        repair = Repair.objects.get(name='Test delete repair')
        response = c.get(f'/repair/delete/{repair.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/repair/delete/{repair.id}', 302)

    def test_loggin(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_with_wrong_repair_id_gets_404_error(self):
        c.login(username=username, password=password)
        response = c.get(f'/repair/delete/2')
        self.assertEqual(response.status_code, 404)

    def test_render_delete_repair_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test delete repair')
        response = c.get(f'/repair/delete/{repair.id}')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test delete repair')
        response = c.get(f'/repair/delete/{repair.id}')
        self.assertTemplateUsed(response, 'Garage/delete_repair.html')

    def test_logged_in_user_successfully_deletes_repair(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test delete repair')
        self.assertEqual(Repair.objects.count(), 1)
        c.post(f'/repair/delete/{repair.id}')
        self.assertEqual(Repair.objects.count(), 0)

    def test_logged_in_user_receives_success_message_after_delete_repair(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test delete repair')
        self.assertEqual(Repair.objects.count(), 1)
        response = c.post(f"/repair/delete/{repair.id}")
        self.assertEqual(Repair.objects.count(), 0)
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "success")
        self.assertEqual(all_messages[0].message, 'Информация о ремонте была успешно удалена!')

    def test_redirect_for_logged_in_user_after_deleted_repair(self):
        c.login(username=username, password=password)
        repair = Repair.objects.get(name='Test delete repair')
        car = Car.objects.get(id=repair.car_id)
        response = c.post(f'/repair/delete/{repair.id}')
        self.assertRedirects(response, f'/car/{car.id}')
