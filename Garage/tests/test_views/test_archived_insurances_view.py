import datetime

from django.test import TestCase, Client

from Garage.models import (
    User,
    Car,
    Insurance
)

c = Client()
username = 'testuser'
password = '1234567890'


class TestInsurancesArchivedView(TestCase):

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

        Insurance.objects.create(
            type='КАСКА',
            policy_number='RO60753F45',
            start_date=datetime.date(2021, 2, 14),
            end_date=datetime.date(2022, 2, 13),
            price=3580.34,
            car_id=second_car.id,
            archive=True
        )

        Insurance.objects.create(
            type='КАСКА',
            start_date=datetime.date(2019, 2, 14),
            end_date=datetime.date(2020, 2, 13),
            price=2521,
            car_id=second_car.id
        )

        Insurance.objects.create(
            type='ОСАГО',
            policy_number='ER594CCD2',
            start_date=datetime.date(2020, 2, 14),
            end_date=datetime.date(2021, 2, 13),
            price=512.34,
            car_id=second_car.id,
            archive=True
        )

        Insurance.objects.create(
            type='ОСАГО',
            start_date=datetime.date(2021, 1, 31),
            end_date=datetime.date(2022, 1, 30),
            price=1099.34,
            car_id=third_car.id,
            archive=True
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get('/insurances/archived/')
        self.assertRedirects(response, f'/accounts/login/?next=/insurances/archived/', 302)

    def test_login(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        response = c.get('/insurances/archived/')
        self.assertEqual(response.context['user'].username, username)

    def test_render_insurances_archived_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/insurances/archived/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/insurances/archived/')
        self.assertTemplateUsed(response, 'Garage/archived_insurances.html')

    def test_logged_in_user_without_car_get_message(self):
        c.login(username=username, password=password)
        response = c.get('/insurances/archived/')
        self.assertEqual(response.context['message'], 'У вас нет автомобилей и страховок')

    def test_logged_in_user_without_archived_insurance_get_message(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/insurances/archived/')
        self.assertEqual(response.context['message'], 'У вас нет страховок в папке архив')

    def test_logged_in_user_receives_archived_insurances(self):
        c.login(username='third-testuser', password=password)
        response = c.get('/insurances/archived/')
        self.assertEqual(len(response.context['page_obj_insurances'].object_list), 3)

    def test_logged_in_user_receives_all_insurances_data(self):
        c.login(username='third-testuser', password=password)
        first_insrnc = Insurance.objects.get(policy_number='RO60753F45')
        second_insrnc = Insurance.objects.get(policy_number='ER594CCD2')
        third_insrnc = Insurance.objects.get(price=1099.34)
        response = c.get('/insurances/archived/')
        insurances = response.context['page_obj_insurances']
        self.assertEqual(len(insurances.object_list), 3)
        self.assertIsNone(response.context['message'])
        self.assertEqual(insurances.object_list[0].type, first_insrnc.type)
        self.assertEqual(insurances.object_list[0].description, first_insrnc.description)
        self.assertEqual(insurances.object_list[0].policy_number, first_insrnc.policy_number)
        self.assertEqual(insurances.object_list[0].start_date, first_insrnc.start_date)
        self.assertEqual(insurances.object_list[0].end_date, first_insrnc.end_date)
        self.assertEqual(insurances.object_list[0].price, first_insrnc.price)
        self.assertTrue(insurances.object_list[0].archive)
        self.assertEqual(insurances.object_list[0].car, first_insrnc.car)

        self.assertEqual(insurances.object_list[1].type, second_insrnc.type)
        self.assertEqual(insurances.object_list[1].description, second_insrnc.description)
        self.assertEqual(insurances.object_list[1].policy_number, second_insrnc.policy_number)
        self.assertEqual(insurances.object_list[1].start_date, second_insrnc.start_date)
        self.assertEqual(insurances.object_list[1].end_date, second_insrnc.end_date)
        self.assertEqual(insurances.object_list[1].price, second_insrnc.price)
        self.assertTrue(insurances.object_list[1].archive)
        self.assertEqual(insurances.object_list[1].car, second_insrnc.car)

        self.assertEqual(insurances.object_list[2].type, third_insrnc.type)
        self.assertEqual(insurances.object_list[2].description, third_insrnc.description)
        self.assertEqual(insurances.object_list[2].policy_number, third_insrnc.policy_number)
        self.assertEqual(insurances.object_list[2].start_date, third_insrnc.start_date)
        self.assertEqual(insurances.object_list[2].end_date, third_insrnc.end_date)
        self.assertEqual(insurances.object_list[2].price, third_insrnc.price)
        self.assertTrue(insurances.object_list[2].archive)
        self.assertEqual(insurances.object_list[2].car, third_insrnc.car)
