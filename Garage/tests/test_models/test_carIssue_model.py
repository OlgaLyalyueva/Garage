import datetime

from django.test import TestCase

from Garage.models import (
    Car,
    User,
    CarIssue
)


class TestCarIssue(TestCase):

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
            transmission=2,
            fuel=2,
            drive_system=2,
            user=user
        )

        CarIssue.objects.create(
            name='Шумит шаровая',
            car=car
        )

    def test_check_car_issue_instance(self):
        car_issue = CarIssue.objects.get(id=1)
        self.assertTrue(isinstance(car_issue, CarIssue))

    def test_meta_label_name(self):
        car_issue = CarIssue.objects.get(id=1)
        meta_label_name = car_issue._meta.verbose_name
        self.assertEqual(meta_label_name, 'Тип неполадки')

    def test_get_verbose_labels(self):
        car_issue = CarIssue.objects.get(id=1)
        name = car_issue._meta.get_field('name').verbose_name
        description = car_issue._meta.get_field('description').verbose_name
        close = car_issue._meta.get_field('close').verbose_name
        self.assertEqual(name, 'Название проблемы')
        self.assertEqual(description, 'Описание')
        self.assertEqual(close, 'Состояние')

    def test_check_save_data_in_db(self):
        car = Car.objects.get(producer='Land Rower')
        car_issue = CarIssue.objects.get(id=1)
        self.assertEqual(car_issue.name, 'Шумит шаровая')
        self.assertFalse(car_issue.close)
        self.assertEqual(car_issue.date, datetime.date.today())
        self.assertEqual(car_issue.car_id, car.id)
        self.assertFalse(car_issue.archive)

    def test_check_max_length_for_name(self):
        car_issue = CarIssue.objects.get(id=1)
        max_length = car_issue._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_description(self):
        car_issue = CarIssue.objects.get(id=1)
        max_length = car_issue._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_add_optional_fields_of_model(self):
        CarIssue.objects.filter(id=1).update(
            description='Шумит справа',
        )
        car_issue = CarIssue.objects.get(id=1)
        self.assertEqual(car_issue.description, 'Шумит справа')
