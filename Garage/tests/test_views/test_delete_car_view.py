from django.test import TestCase, Client

from Garage.models import User, Car


class TestDeleteCar(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True,
            is_staff=True
        )
        user.set_password('1234567890')
        user.save()

        Car.objects.create(
            producer='Test delete producer',
            model='Test delete model',
            year=1990,
            transmission=1,
            fuel=3,
            drive_system=2,
            user=user
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        car = Car.objects.get(producer='Test delete producer')
        response = c.get(f'/car/delete/{car.id}')
        self.assertRedirects(response, f'/accounts/login/?next=/car/delete/{car.id}', 302)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        car = Car.objects.get(producer='Test delete producer')
        response = c.get(f'/car/delete/{car.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Garage/delete_car.html')

    def test_redirect_for_logged_in_user_after_deleted_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        car = Car.objects.get(producer='Test delete producer', user_id=user.id)
        response = c.post(f'/car/delete/{car.id}')
        self.assertRedirects(response, '/cars/')
