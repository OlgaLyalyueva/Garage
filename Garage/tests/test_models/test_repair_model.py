import datetime

from django.test import TestCase

from Garage.models import Car, Repair, User


class TestRepair(TestCase):

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

        Repair.objects.create(
            type_of_repair=1,
            name='Замена масла',
            date=datetime.date.today(),
            car=car
        )

    def test_check_repair_instance(self):
        repair = Repair.objects.get(id=1)
        self.assertTrue(isinstance(repair, Repair))

    def test_meta_label_name(self):
        repair = Repair.objects.get(id=1)
        label_name = repair._meta.verbose_name
        self.assertEqual(label_name, 'Ремонт')

    def test_get_verbose_labels(self):
        repair = Repair.objects.get(id=1)
        name = repair._meta.get_field('name').verbose_name
        description = repair._meta.get_field('description').verbose_name
        note = repair._meta.get_field('note').verbose_name
        mileage = repair._meta.get_field('mileage').verbose_name
        price = repair._meta.get_field('price').verbose_name
        self.assertEqual(name, 'Название')
        self.assertEqual(description, 'Описание')
        self.assertEqual(note, 'Примечание')
        self.assertEqual(mileage, 'Пробег')
        self.assertEqual(price, 'Стоимость')

    def test_check_max_length_for_name(self):
        repair = Repair.objects.get(id=1)
        max_length = repair._meta.get_field('name').max_length
        self.assertEqual(max_length, 400)

    def test_check_max_length_for_description(self):
        repair = Repair.objects.get(id=1)
        max_length = repair._meta.get_field('description').max_length
        self.assertEqual(max_length, 2000)

    def test_check_max_length_for_note(self):
        repair = Repair.objects.get(id=1)
        max_length = repair._meta.get_field('note').max_length
        self.assertEqual(max_length, 500)

    def test_check_save_data_in_db(self):
        repair = Repair.objects.get(id=1)
        self.assertEqual(repair.type_of_repair, 1)
        self.assertEqual(repair.name, 'Замена масла')
        self.assertEqual(repair.description, None)
        self.assertEqual(repair.note, None)
        self.assertEqual(repair.mileage, None)
        self.assertEqual(repair.date, datetime.date.today())
        self.assertEqual(repair.car_id, 1)
        self.assertEqual(repair.price, None)
        self.assertFalse(repair.archive)

    def test_add_optional_fields_of_model(self):
        repair_before_update = Repair.objects.get(name='Замена масла')
        Repair.objects.filter(id=1).update(
            description='Масло в коробке',
            note='Проверить клапан',
            mileage=120000,
            price=2100,
        )
        r = Repair.objects.get(id=1)
        self.assertEqual(r.type_of_repair, repair_before_update.type_of_repair)
        self.assertEqual(r.name, repair_before_update.name)
        self.assertEqual(r.description, 'Масло в коробке')
        self.assertEqual(r.note, 'Проверить клапан')
        self.assertEqual(r.mileage, 120000)
        self.assertEqual(r.price, 2100)
        self.assertEqual(r.date, repair_before_update.date)
        self.assertEqual(r.car_id, repair_before_update.car_id)
