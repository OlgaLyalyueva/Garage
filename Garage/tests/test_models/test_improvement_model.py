import datetime

from django.test import TestCase

from Garage.models import (
    Car,
    User,
    Improvement
)


class TestImprovement(TestCase):

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

        Improvement.objects.create(
            name='Поменять лампочки в фарах',
            car=car
        )

    def test_check_improvement_instance(self):
        improvement = Improvement.objects.get(id=1)
        self.assertTrue(isinstance(improvement, Improvement))

    def test_meta_label_name(self):
        improvement = Improvement.objects.get(id=1)
        meta_label_name = improvement._meta.verbose_name
        self.assertEqual(meta_label_name, 'Улучшение')

    def test_get_verbose_labels(self):
        improvement = Improvement.objects.get(id=1)
        name = improvement._meta.get_field('name').verbose_name
        description = improvement._meta.get_field('description').verbose_name
        close = improvement._meta.get_field('close').verbose_name
        price = improvement._meta.get_field('price').verbose_name
        self.assertEqual(name, 'Название проблемы')
        self.assertEqual(description, 'Описание')
        self.assertEqual(close, 'Состояние')
        self.assertEqual(price, 'Стоимость')

    def test_check_save_data_in_db(self):
        improvement = Improvement.objects.get(id=1)
        self.assertEqual(improvement.date, datetime.date.today())
        self.assertEqual(improvement.name, 'Поменять лампочки в фарах')
        self.assertFalse(improvement.close)
        self.assertFalse(improvement.archive)
        self.assertTrue(improvement.car)

    def test_check_max_length_for_name(self):
        improvement = Improvement.objects.get(id=1)
        max_length = improvement._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_description(self):
        improvement = Improvement.objects.get(id=1)
        max_length = improvement._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_add_optional_fields_of_model(self):
        Improvement.objects.filter(id=1).update(
            description=' ',
            price=1800
        )
        improvement = Improvement.objects.get(id=1)
        self.assertEqual(improvement.description, ' ')
        self.assertEqual(improvement.price, 1800)
        self.assertFalse(improvement.archive)
