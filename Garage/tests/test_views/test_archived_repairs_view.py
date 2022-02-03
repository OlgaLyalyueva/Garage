import datetime

from django.test import TestCase, Client

from Garage.models import (
    User,
    Car,
    Repair
)

c = Client()
username = 'testuser'
password = '1234567890'


class TestRepairsArchivedView(TestCase):

    @classmethod
    def setUpTestData(cls):
        first_user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True
        )
        first_user.set_password('1234567890')
        first_user.save()

        second_user = User.objects.create_user(
            username='second-testuser',
            first_name='Test 2',
            last_name='T 2',
            email='test+2@test.test',
            is_active=True
        )
        second_user.set_password('1234567890')
        second_user.save()

        third_user = User.objects.create_user(
            username='third-testuser',
            first_name='Test 3',
            last_name='T 3',
            email='test+3@test.test',
            is_active=True
        )
        third_user.set_password('1234567890')
        third_user.save()

        Car.objects.create(
            producer='Test Land Rover',
            model='Discovery Sport',
            year=2016,
            transmission='автомат',
            fuel=2,
            drive_system=1,
            user=second_user
        )

        second_car = Car.objects.create(
            producer='Test Nissan',
            model='X-Trail',
            year=2010,
            transmission='автомат',
            fuel=2,
            drive_system=2,
            archive=True,
            user=third_user
        )

        third_car = Car.objects.create(
            producer='Test Audi',
            model='Q7',
            year=2020,
            transmission='автомат',
            fuel=5,
            drive_system=1,
            user=third_user
        )

        Repair.objects.create(
            type_of_repair=1,
            name='замена масла',
            description='масло GT12',
            note='полная замена',
            mileage=12400,
            price=349.45,
            date=datetime.date(2012, 4, 5),
            car_id=second_car.id,
            archive=True
        )

        Repair.objects.create(
            type_of_repair=1,
            name='замена фильтров',
            mileage=345900,
            car_id=second_car.id,
            date=datetime.date(2021, 4, 30),
            archive=True
        )

        Repair.objects.create(
            type_of_repair=2,
            name='ремонт рулевой рейки',
            description='отдать Роману',
            mileage=237089,
            date=datetime.date(2021, 4, 30),
            car_id=second_car.id
        )

        Repair.objects.create(
            type_of_repair=3,
            name='поклейка пленки на капот',
            date=datetime.date(2021, 4, 30),
            car_id=third_car.id,
            archive=True
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get('/repairs/archived/')
        self.assertRedirects(response, f'/accounts/login/?next=/repairs/archived/', 302)

    def test_login(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_render_repairs_archived_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/repairs/archived/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/repairs/archived/')
        self.assertTemplateUsed(response, 'Garage/archived_repairs.html')

    def test_logged_in_user_without_car_get_message(self):
        c.login(username=username, password=password)
        response = c.get('/repairs/archived/')
        self.assertEqual(response.context['message'], 'У вас нет автомобилей и ремонтов')

    def test_logged_in_user_without_archived_repairs_get_message(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/repairs/archived/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных ремонтов в папке архив')

    def test_logged_in_user_receives_archived_repairs(self):
        c.login(username='third-testuser', password=password)
        response = c.get('/repairs/archived/')
        self.assertEqual(len(response.context['page_obj_repairs']), 3)

    def test_logged_in_user_receives_all_repairs_data(self):
        c.login(username='third-testuser', password=password)
        first_repair = Repair.objects.get(name='замена масла')
        second_repair = Repair.objects.get(name='замена фильтров')
        third_repair = Repair.objects.get(name='поклейка пленки на капот')
        response = c.get('/repairs/archived/')
        repair = response.context['page_obj_repairs']
        self.assertEqual(len(repair.object_list), 3)
        self.assertIsNone(response.context['message'])
        self.assertEqual(repair.object_list[0].type_of_repair, first_repair.type_of_repair)
        self.assertEqual(repair.object_list[0].name, first_repair.name)
        self.assertEqual(repair.object_list[0].description, first_repair.description)
        self.assertEqual(repair.object_list[0].note, first_repair.note)
        self.assertEqual(repair.object_list[0].mileage, first_repair.mileage)
        self.assertEqual(repair.object_list[0].price, first_repair.price)
        self.assertTrue(repair.object_list[0].archive)
        self.assertEqual(repair.object_list[0].car, first_repair.car)

        self.assertEqual(repair.object_list[1].type_of_repair, second_repair.type_of_repair)
        self.assertEqual(repair.object_list[1].name, second_repair.name)
        self.assertEqual(repair.object_list[1].mileage, second_repair.mileage)
        self.assertTrue(repair.object_list[1].archive)
        self.assertEqual(repair.object_list[1].car, second_repair.car)

        self.assertEqual(repair.object_list[2].type_of_repair, third_repair.type_of_repair)
        self.assertEqual(repair.object_list[2].name, third_repair.name)
        self.assertTrue(repair.object_list[2].archive)
        self.assertEqual(repair.object_list[2].car, third_repair.car)
