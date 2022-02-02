import datetime

from django.test import TestCase

from Garage.models import User, Car, Repair
from django.test import Client


class TestRepairs(TestCase):

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

    def test_not_logged_in_user_redirect_to_login_page(self):
        c = Client()
        response = c.get('/repairs/')
        self.assertRedirects(response, '/accounts/login/?next=/repairs/', 302)

    def test_view_exists_for_logged_in_user_without_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/repairs/')
        self.assertEqual(response.status_code, 200)

    def test_view_exists_for_logged_in_user_without_repair(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        Car.objects.create(
            producer='Test repair producer',
            model='Test repair model',
            year=1998,
            transmission=9,
            fuel=2,
            drive_system=3,
            user=user
        )

        response = c.get('/repairs/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/repairs/')
        self.assertTemplateUsed(response, 'Garage/repairs.html')

    def test_for_logged_in_user_receives_repairs_that_are_not_archived(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')

        car = Car.objects.create(
            producer='Test repair producer',
            model='Test repair model',
            year=1998,
            transmission=9,
            fuel=2,
            drive_system=3,
            user=user
        )

        Repair.objects.create(
            type_of_repair=2,
            name='Test repair name',
            description='Test description',
            note='Test note',
            mileage=120,
            price=2313.08,
            date=datetime.date.today(),
            car=car
        )

        Repair.objects.create(
            type_of_repair=3,
            name='Test repair name',
            date=datetime.date(2021, 1, 31),
            car=car
        )

        Repair.objects.create(
            type_of_repair=1,
            name='Test Second repair name',
            description='Test description',
            archive=True,
            date=datetime.date(2020, 12, 30),
            car=car
        )

        response = c.get('/repairs/')
        self.assertEqual(response.status_code, 200)
        cars = response.context['cars']
        self.assertEqual(len(cars), 1)
        repairs = response.context['page_obj_repairs']
        self.assertEqual(len(repairs.object_list), 2)


    def test_repairs_are_sent_to_archive_if_car_is_moved_to_archive(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')

        car = Car.objects.create(
            producer='Test repair producer',
            model='Test repair model',
            year=1998,
            transmission=9,
            fuel=2,
            drive_system=3,
            user=user
        )

        Repair.objects.create(
            type_of_repair=2,
            name='Test repair name',
            description='Test description',
            price=13,
            date=datetime.date(2021, 11, 6),
            car=car
        )

        Repair.objects.create(
            type_of_repair=2,
            name='Test Second repair name',
            description='',
            note='Test note',
            mileage=34000,
            price=1,
            date=datetime.date.today(),
            car=car
        )
        response = c.get('/repairs/')
        repairs = response.context['page_obj_repairs']
        self.assertEqual(len(repairs.object_list), 2)
        car.archive = True
        car.save()
        response = c.get('/repairs/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей и ремонтов')
