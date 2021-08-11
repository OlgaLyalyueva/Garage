import datetime

from django.test import TestCase, Client
from Garage.models import User, Car, CarIssue

c = Client()
username = 'testuser'
password = '1234567890'


class TestCarIssues(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='testuser',
            is_active=True,
            is_staff=True
        )

        user.set_password('1234567890')
        user.save()

    def test_not_logged_in_user_redirect_to_login_page(self):
        response = c.get('/issues/')
        self.assertRedirects(response, '/accounts/login/?next=/issues/', 302)

    def test_logged_in(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_logged_in_user_receives_view(self):
        c.login(username=username, password=password)
        response = c.get('/issues/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/issues/')
        self.assertTemplateUsed(response, 'Garage/car_issues.html')

    def test_logged_in_user_without_car_receives_message(self):
        c.login(username=username, password=password)
        user = User.objects.get(username=username)
        cars = Car.objects.filter(user_id=user.id)
        response = c.get('/issues/')
        if len(cars) == 0:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей')

    def test_logged_in_user_without_carissue_receives_message(self):
        user = User.objects.get(username=username)
        Car.objects.create(
            producer='Test car issue',
            model='Test car issue model',
            year=1825,
            transmission=3,
            fuel=2,
            drive_system=1,
            user=user
        )

        Car.objects.create(
            producer='Test car issue',
            model='Test car issue model',
            year=1825,
            transmission=3,
            fuel=2,
            drive_system=1,
            archive=True,
            user=user
        )

        c.login(username=username, password=password)
        cars = Car.objects.filter(user_id=user.id, archive=False)
        issues = {}
        response = c.get('/issues/')
        if cars:
            for car in cars:
                issues[car.id] = CarIssue.objects.filter(car_id=car.id, archive=False)
                if not issues:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(Car.objects.count(), 1)
                    self.assertEqual(len(response.context['cars']), 1)
                    self.assertEqual(response.context['message'], 'У вас нет текущих проблем')

    def test_logged_in_user_receives_issue(self):
        user = User.objects.get(username=username)
        car = Car.objects.create(
            producer='Test car issue',
            model='Test car issue model',
            year=1825,
            transmission=3,
            fuel=2,
            drive_system=1,
            user=user
        )

        CarIssue.objects.create(
            name='Test CarIssue',
            car=car
        )

        c.login(username=username, password=password)
        cars = Car.objects.filter(user_id=user.id, archive=False)
        issues = {}
        response = c.get('/issues/')
        if cars:
            for car in cars:
                issues[car.id] = CarIssue.objects.filter(car_id=car.id, archive=False)
                if issues:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(Car.objects.count(), 1)
                    self.assertEqual(CarIssue.objects.count(), 1)
                    # добавить проверку для контекста

    def test_logged_in_user_receives_issues(self):
        user = User.objects.get(username=username)
        first_car = Car.objects.create(
            producer='Test first car producer',
            model='Test first car model',
            year=19001,
            transmission=3,
            fuel=2,
            drive_system=1,
            user=user
        )

        second_car = Car.objects.create(
            producer='Test second car producer',
            model='Test second car model',
            year=19001,
            transmission=3,
            fuel=2,
            drive_system=1,
            user=user
        )

        CarIssue.objects.create(
            name='Test First CarIssue',
            car=first_car
        )

        CarIssue.objects.create(
            name='Test Second CarIssue',
            description='Test description for second car',
            date=datetime.date(2021, 8, 9),
            state=False,
            car=second_car
        )

        c.login(username=username, password=password)
        cars = Car.objects.filter(user_id=user.id, archive=False)
        issues = {}
        response = c.get('/issues/')
        if cars:
            for car in cars:
                issues[car.id] = CarIssue.objects.filter(car_id=car.id, archive=False)
                if issues:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(Car.objects.count(), 2)
                    self.assertEqual(CarIssue.objects.count(), 2)
                    # добавить проверку для контекста
