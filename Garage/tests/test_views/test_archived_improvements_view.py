from django.test import TestCase, Client

from Garage.models import (
    User,
    Car,
    Improvement
)

c = Client()
username = 'testuser'
password = '1234567890'


class TestImprovementsArchivedView(TestCase):

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
            producer='Test Infinity',
            model='RX',
            year=2020,
            transmission=2,
            fuel=2,
            drive_system=1,
            user=second_user
        )

        second_car = Car.objects.create(
            producer='Test Kia',
            model='Rio',
            year=2010,
            transmission=2,
            fuel=2,
            drive_system=2,
            archive=True,
            user=third_user
        )

        third_car = Car.objects.create(
            producer='Test Jeep',
            model='Renegade',
            year=2017,
            transmission=1,
            fuel=5,
            drive_system=1,
            user=third_user
        )

        Improvement.objects.create(
            name='Замена ремня',
            car_id=second_car.id,
            archive=True
        )

        Improvement.objects.create(
            name='Замена масла',
            description='коробка передач',
            price=1900,
            close=True,
            car_id=second_car.id
        )

        Improvement.objects.create(
            name='Защита на двигатель',
            description='Подобрать защиту на двигатель, проверить какая ставится с завода: пластик или метал.',
            price=0,
            car_id=second_car.id,
            archive=True
        )

        Improvement.objects.create(
            name='Тонировка',
            description='Затонировать задние двери и растонировать передние',
            price=3987,
            car_id=third_car.id,
            archive=True,
            close=True
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        response = c.get('/improvements/archived/')
        self.assertRedirects(response, f'/accounts/login/?next=/improvements/archived/', 302)

    def test_login(self):
        logged_in = c.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_render_improvements_archived_view_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/improvements/archived/')
        self.assertEqual(response.status_code, 200)

    def test_render_template_for_logged_in_user(self):
        c.login(username=username, password=password)
        response = c.get('/improvements/archived/')
        self.assertTemplateUsed(response, 'Garage/archived_improvements.html')

    def test_logged_in_user_without_car_get_message(self):
        c.login(username=username, password=password)
        response = c.get('/improvements/archived/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей')

    def test_logged_in_user_without_archived_improvement_get_message(self):
        c.login(username='second-testuser', password=password)
        response = c.get('/improvements/archived/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных улучшений в папке архив')

    def test_logged_in_user_receives_archived_improvements(self):
        c.login(username='third-testuser', password=password)
        response = c.get('/improvements/archived/')
        self.assertEqual(len(response.context['page_obj_improvements'].object_list), 3)

    def test_logged_in_user_receives_all_improvements_data(self):
        c.login(username='third-testuser', password=password)
        first_impr = Improvement.objects.get(name='Замена ремня')
        second_impr = Improvement.objects.get(name='Защита на двигатель')
        third_impr = Improvement.objects.get(name='Тонировка')
        response = c.get('/improvements/archived/')
        improvements = response.context['page_obj_improvements']
        self.assertEqual(len(improvements.object_list), 3)
        self.assertIsNone(response.context['message'])
        self.assertEqual(improvements.object_list[0].name, first_impr.name)
        self.assertEqual(improvements.object_list[0].description, first_impr.description)
        self.assertEqual(improvements.object_list[0].date, first_impr.date)
        self.assertEqual(improvements.object_list[0].price, first_impr.price)
        self.assertTrue(improvements.object_list[0].archive)
        self.assertFalse(improvements.object_list[0].close)
        self.assertEqual(improvements.object_list[0].car, first_impr.car)

        self.assertEqual(improvements.object_list[1].name, second_impr.name)
        self.assertEqual(improvements.object_list[1].description, second_impr.description)
        self.assertEqual(improvements.object_list[1].date, second_impr.date)
        self.assertEqual(improvements.object_list[1].price, second_impr.price)
        self.assertTrue(improvements.object_list[1].archive)
        self.assertFalse(improvements.object_list[1].close)
        self.assertEqual(improvements.object_list[1].car, second_impr.car)

        self.assertEqual(improvements.object_list[2].name, third_impr.name)
        self.assertEqual(improvements.object_list[2].description, third_impr.description)
        self.assertEqual(improvements.object_list[2].date, third_impr.date)
        self.assertEqual(improvements.object_list[2].price, third_impr.price)
        self.assertTrue(improvements.object_list[2].archive)
        self.assertTrue(improvements.object_list[2].close)
        self.assertEqual(improvements.object_list[2].car, third_impr.car)
