import datetime

from django.test import TestCase

from Garage.models import (
    Car,
    User,
    Insurance
)


class TestInsurance(TestCase):

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
            producer='Nissan',
            model='X-trail',
            year=2010,
            transmission='автомат',
            fuel=2,
            drive_system=1,
            user=user
        )

        Insurance.objects.create(
            type='ОСАГО',
            start_date=datetime.date(2021, 3, 1),
            end_date=datetime.date(2021, 2, 28),
            price=600,
            car=car
        )

    def test_check_insurance_instance(self):
        insurance = Insurance.objects.get(id=1)
        self.assertTrue(isinstance(insurance, Insurance))

    def test_meta_label_name(self):
        insurance = Insurance.objects.get(id=1)
        meta_label_name = insurance._meta.verbose_name
        self.assertEqual(meta_label_name, 'Страховка')

    def test_get_verbose_labels(self):
        insurance = Insurance.objects.get(id=1)
        type_label = insurance._meta.get_field('type').verbose_name
        description_label = insurance._meta.get_field('description').verbose_name
        policy_number_label = insurance._meta.get_field('policy_number').verbose_name
        start_date_label = insurance._meta.get_field('start_date').verbose_name
        end_date_label = insurance._meta.get_field('end_date').verbose_name
        price_label = insurance._meta.get_field('price').verbose_name
        self.assertEqual(type_label, 'Тип страховки')
        self.assertEqual(description_label, 'Описание')
        self.assertEqual(policy_number_label, 'Номер страховки')
        self.assertEqual(start_date_label, 'Дата начала')
        self.assertEqual(end_date_label, 'Дата окончания')
        self.assertEqual(price_label, 'Стоимость страховки')

    def test_check_save_data_in_db(self):
        insurance = Insurance.objects.get(id=1)
        self.assertEqual(insurance.type, 'ОСАГО')
        self.assertEqual(insurance.start_date, datetime.date(2021, 3, 1))
        self.assertEqual(insurance.end_date, datetime.date(2021, 2, 28))
        self.assertEqual(insurance.price, 600)
        self.assertTrue(insurance.car)
        self.assertEqual(insurance.archive, False)

    def test_check_max_length_for_producer(self):
        insurance = Insurance.objects.get(id=1)
        max_length = insurance._meta.get_field('type').max_length
        self.assertEqual(max_length, 255)

    def test_check_max_length_for_model(self):
        insurance = Insurance.objects.get(id=1)
        max_length = insurance._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    def test_add_optional_fields_of_model(self):
        Insurance.objects.filter(id=1).update(
            description='ОСАГО Тас Банк',
            policy_number='AC23056',
            price=121.31,
        )
        insurance = Insurance.objects.get(id=1)
        self.assertEqual(insurance.description, 'ОСАГО Тас Банк')
        self.assertEqual(insurance.policy_number, 'AC23056')
        self.assertEqual(insurance.price, 121.31)
        self.assertTrue(insurance.type)
