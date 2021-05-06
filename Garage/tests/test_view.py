from django.test import TestCase
from Garage.models import User
from django.test import Client

class TestCarsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True
        )
        user.set_password('1234567890')
        user.save()

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_render_cars_view_user_logged_in(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.status_code, 200)
