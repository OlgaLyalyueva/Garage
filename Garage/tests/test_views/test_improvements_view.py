from django.test import TestCase

from Garage.models import User, Car, Improvement
from django.test import Client


class TestImprovements(TestCase):

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
        response = c.get('/improvements/')
        self.assertRedirects(response, '/accounts/login/?next=/improvements/', 302)

    def test_view_exists_for_logged_in_user_without_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/improvements/')
        self.assertEqual(response.status_code, 200)

    def test_view_exists_for_logged_in_user_without_improvement(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        Car.objects.create(
            producer='Test improvement producer',
            model='Test improvement model',
            year=1998,
            transmission=5,
            fuel=2,
            drive_system=1,
            user=user
        )

        response = c.get('/improvements/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/improvements/')
        self.assertTemplateUsed(response, 'Garage/improvements.html')

    def test_for_logged_in_user_receives_improvements_that_are_not_archived(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')

        car = Car.objects.create(
            producer='Test improvement producer',
            model='Test improvement model',
            year=1998,
            transmission=5,
            fuel=2,
            drive_system=1,
            user=user
        )

        Improvement.objects.create(
            name='Test Improvement name',
            description='Test description',
            price=2313.08,
            car=car
        )

        Improvement.objects.create(
            name='Test Improvement name',
            car=car
        )

        Improvement.objects.create(
            name='Test Second Improvement name',
            description='Test description',
            car=car
        )

        response = c.get('/improvements/')
        self.assertEqual(response.status_code, 200)
        cars = response.context['cars']
        self.assertEqual(len(cars), 1)
        improvements = response.context['improvements']
        self.assertEqual(len(improvements[0]), 3)


    def test_improvements_are_sent_to_archive_if_car_is_moved_to_archive(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')

        car = Car.objects.create(
            producer='Test improvement producer',
            model='Test improvement model',
            year=1998,
            transmission=5,
            fuel=2,
            drive_system=1,
            user=user
        )

        Improvement.objects.create(
            name='Test Improvement name',
            description='Test description',
            price=13,
            car=car
        )

        Improvement.objects.create(
            name='Test Second Improvement name',
            description='',
            price=1,
            car=car
        )
        response = c.get('/improvements/')
        improvements = response.context['improvements']
        self.assertEqual(len(improvements[0]), 2)
        car.archive = True
        car.save()
        response = c.get('/improvements/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей и улучшений')
