import datetime

from django.test import TestCase, Client

from Garage.models import (
    User,
    Car,
    CarIssue
)

c = Client()
username = 'testuser'
password = '1234567890'


class TestCarIssuesArchivedView(TestCase):

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

        CarIssue.objects.create(
            name='Тонировка',
            description='легкое тонирование',
            date=datetime.date(2021, 2, 1),
            close=True,
            car_id=second_car.id,
            archive=True
        )

        CarIssue.objects.create(
            name='Перетяжка сидений',
            date=datetime.date(2019, 2, 14),
            close=True,
            car_id=second_car.id,
            archive=True
        )

        CarIssue.objects.create(
            name='замена ресничек',
            description='правая фара',
            date=datetime.date(2020, 2, 29),
            car_id=second_car.id
        )

        CarIssue.objects.create(
            name='замена дворников',
            date=datetime.date(2021, 9, 1),
            car_id=third_car.id,
            archive=True
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get('/issues/archived/')
        self.assertRedirects(response, f'/accounts/login/?next=/issues/archived/', 302)

    def test_login(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c.login(username=username, password=password)
        response = c.get('/issues/archived/')
        self.assertEqual(response.context['user'].username, username)

    def test_render_issues_archived_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/issues/archived/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/issues/archived/')
        self.assertTemplateUsed(response, 'Garage/archived_issues.html')

    def test_logged_in_user_without_car_get_message(self):
        c.login(username=username, password=password)
        response = c.get('/issues/archived/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей')

    def test_logged_in_user_without_archived_issues_get_message(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/issues/archived/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных поломок в папке архив')

    def test_logged_in_user_receives_archived_issues(self):
        c.login(username='third-testuser', password=password)
        response = c.get('/issues/archived/')
        self.assertEqual(len(response.context['issues']), 2)

    def test_logged_in_user_receives_all_issues_data(self):
        c.login(username='third-testuser', password=password)
        first_issue = CarIssue.objects.get(name='Тонировка')
        second_issue = CarIssue.objects.get(name='Перетяжка сидений')
        third_issue = CarIssue.objects.get(name='замена дворников')
        response = c.get('/issues/archived/')
        issues = response.context['issues']
        self.assertEqual(len(issues), 2)
        self.assertIsNone(response.context['message'])
        self.assertEqual(issues[0][0].name, first_issue.name)
        self.assertEqual(issues[0][0].description, first_issue.description)
        self.assertEqual(issues[0][0].date, first_issue.date)
        self.assertTrue(issues[0][0].close)
        self.assertTrue(issues[0][0].archive)
        self.assertEqual(issues[0][0].car, first_issue.car)

        self.assertEqual(issues[0][1].name, second_issue.name)
        self.assertEqual(issues[0][1].description, second_issue.description)
        self.assertEqual(issues[0][1].date, second_issue.date)
        self.assertTrue(issues[0][1].close)
        self.assertTrue(issues[0][1].archive)
        self.assertEqual(issues[0][1].car, second_issue.car)

        self.assertEqual(issues[1][0].name, third_issue.name)
        self.assertEqual(issues[1][0].description, third_issue.description)
        self.assertEqual(issues[1][0].date, third_issue.date)
        self.assertFalse(issues[1][0].close)
        self.assertTrue(issues[1][0].archive)
        self.assertEqual(issues[1][0].car, third_issue.car)
