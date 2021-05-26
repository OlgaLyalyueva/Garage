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

    def test_add_optional_fields_of_model(self):
        Repair.objects.filter(id=1).update(
            description='Масло в коробке',
            note='Проверить клапан',
            mileage=120000,
            price=2100,
        )
        r = Repair.objects.get(id=1)
        self.assertEqual(r.description, 'Масло в коробке')
        self.assertEqual(r.note, 'Проверить клапан')
        self.assertEqual(r.mileage, 120000)
        self.assertEqual(r.price, 2100)
