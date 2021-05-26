from django.test import TestCase

from Garage.models import Body


class TestBody(TestCase):

    @classmethod
    def setUpTestData(cls):
        Body.objects.create(
            name='Купе'
        )

    def test_check_body_instance(self):
        body = Body.objects.get(name='Купе')
        self.assertTrue(isinstance(body, Body))

    def test_meta_label_name(self):
        body = Body.objects.get(id=1)
        name_label = body._meta.verbose_name
        self.assertEqual(name_label, 'Тип кузова')

    def test_get_verbose_labels(self):
        body = Body.objects.get(id=1)
        name_label = body._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Тип кузова')

    def test_check_save_data_in_db(self):
        body = Body.objects.get(id=1)
        self.assertEqual(body.name, 'Купе')

    def test_check_max_length_for_name(self):
        body = Body.objects.get(id=1)
        max_length = body._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)
