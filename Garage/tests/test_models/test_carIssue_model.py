from django.test import TestCase

from Garage.models import (
    Car,
    User,
    CarProblem
)


class TestCarProblem(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            password='1234567890wW',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
            email='test@test.test'
        )

        car = Car.objects.create(
            producer='Land Rower',
            model='Discovery Sport',
            year=2013,
            transmission='автомат',
            fuel=2,
            drive_system=2,
            user=user
        )

        CarProblem.objects.create(
            name='Шумит шаровая',
            car=car
        )

    def test_check_car_problem_instance(self):
        car_problem = CarProblem.objects.get(id=1)
        self.assertTrue(isinstance(car_problem, CarProblem))

    def test_meta_label_name(self):
        car_problem = CarProblem.objects.get(id=1)
        meta_label_name = car_problem._meta.verbose_name
        self.assertEqual(meta_label_name, 'Тип неполадки')

    def test_get_verbose_labels(self):
        car_problem = CarProblem.objects.get(id=1)
        name = car_problem._meta.get_field('name').verbose_name
        description = car_problem._meta.get_field('description').verbose_name
        state = car_problem._meta.get_field('state').verbose_name
        self.assertEqual(name, 'Название проблемы')
        self.assertEqual(description, 'Описание')
        self.assertEqual(state, 'Состояние')

    def test_check_save_data_in_db(self):
        car_problem = CarProblem.objects.get(id=1)
        self.assertEqual(car_problem.name, 'Шумит шаровая')
        self.assertTrue(car_problem.state)
        self.assertTrue(car_problem.date)
        self.assertTrue(car_problem.car)

    def test_check_max_length_for_name(self):
        car_problem = CarProblem.objects.get(id=1)
        max_length = car_problem._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_description(self):
        car_problem = CarProblem.objects.get(id=1)
        max_length = car_problem._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_add_optional_fields_of_model(self):
        CarProblem.objects.filter(id=1).update(
            description='Шумит справа',
        )
        car_problem = CarProblem.objects.get(id=1)
        self.assertEqual(car_problem.description, 'Шумит справа')
