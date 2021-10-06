from django.test import TestCase

from Garage.models import Engine


class TestEngine(TestCase):
    @classmethod
    def setUpTestData(cls):
        Engine.objects.create(
            name='2.5'
        )

    def test_check_engine_instance(self):
        engine = Engine.objects.get(name='2.5')
        self.assertTrue(isinstance(engine, Engine))

    def test_meta_label_name(self):
        engine = Engine.objects.get(name='2.5')
        name_label = engine._meta.verbose_name
        self.assertEqual(name_label, 'Тип двигателя')

    def test_get_verbose_labels(self):
        engine = Engine.objects.get(name='2.5')
        name_label = engine._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'Тип двигателя')

    def test_check_save_data_in_db(self):
        engine = Engine.objects.get(name='2.5')
        self.assertEqual(engine.name, '2.5')

    def test_check_max_length_for_name(self):
        engine = Engine.objects.get(name='2.5')
        max_length = engine._meta.get_field('name').max_length
        self.assertEquals(max_length, 500)
