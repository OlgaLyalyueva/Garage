from datetime import date

from django.test import TestCase, Client

from Garage.models import (
    Car,
    User,
    CarIssue,
    Insurance,
    Improvement,
    Repair
)


class TestCarView(TestCase):

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
            producer='Test Car with insurance, improvement, repair, car problems',
            model='X car',
            year=1999,
            transmission='автомат',
            fuel=5,
            drive_system=2,
            user=user
        )

        Car.objects.create(
            producer='Test car',
            model='CRV',
            year=2000,
            transmission='типтроник',
            fuel=9,
            drive_system=2,
            user=user
        )

        CarIssue.objects.create(
            name='Test car problem',
            description='Test description',
            close=True,
            date=date.today(),
            car_id=car.id
        )

        Insurance.objects.create(
            type='Test ОСАГО',
            policy_number='AP456789',
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
            price=599.43,
            car_id=car.id
        )

        Improvement.objects.create(
            name='Test name',
            car_id=car.id
        )

        Repair.objects.create(
            type_of_repair=2,
            name='Лобовое стекло',
            price=7699,
            date=date.today(),
            car_id=car.id
        )

        Repair.objects.create(
            type_of_repair=1,
            name='Замена масла в коробке',
            description='ATF SP-III',
            mileage=80000,
            price=1500.05,
            date=date.today(),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        car = Car.objects.get(producer='Test car')
        response = c.get(f'/car/{car.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/car/{car.id}', 302)

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test car')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_render_car_view_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test car')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_receives_car_issue_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test Car with insurance, improvement, repair, car problems')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(response.context['car_issue'][0].name, 'Test car problem')
        self.assertEqual(response.context['car_issue'][0].description, 'Test description')
        self.assertTrue(response.context['car_issue'][0].close)
        self.assertEqual(response.context['car_issue'][0].date, date.today())
        self.assertFalse(response.context['car_issue'][0].archive)

    def test_logged_in_user_receives_insurances_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test Car with insurance, improvement, repair, car problems')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(response.context['insurances'][0].type, 'Test ОСАГО')
        self.assertEqual(response.context['insurances'][0].policy_number, 'AP456789')
        self.assertEqual(response.context['insurances'][0].start_date, date(2021, 1, 1))
        self.assertEqual(response.context['insurances'][0].end_date, date(2021, 12, 31))
        self.assertEqual(response.context['insurances'][0].price, 599.43)
        self.assertFalse(response.context['insurances'][0].archive)

    def test_logged_in_user_receives_improvement_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test Car with insurance, improvement, repair, car problems')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(response.context['improvement'][0].name, 'Test name')
        self.assertFalse(response.context['improvement'][0].close)
        self.assertEqual(response.context['improvement'][0].date, date.today())
        self.assertFalse(response.context['improvement'][0].archive)

    def test_logged_in_user_receives_two_repair_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test Car with insurance, improvement, repair, car problems')
        response = c.get(f'/car/{car.id}')
        self.assertEqual(len(response.context['repair']), 2)
