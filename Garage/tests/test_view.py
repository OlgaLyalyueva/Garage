from django.test import TestCase

from Garage.models import User, Car, Body, Engine, CarProblem, Improvement, Insurance, Repair
from django.test import Client
from datetime import date
from Garage.forms import CarForm


class TestCarsView(TestCase):

    @classmethod
    def setUpTestData(cls):
        first_user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True
        )
        first_user.set_password('1234567890')
        first_user.save()

        second_user = User.objects.create_user(
            username='second-testuser',
            first_name='Test 2',
            last_name='T 2',
            email='test+2@test.test',
            is_active=True
        )
        second_user.set_password('1234567890')
        second_user.save()

        body = Body.objects.create(
            name='Test body name'
        )

        engine = Engine.objects.create(
            name='Test engine name'
        )

        Car.objects.create(
            producer='Test Tesla',
            model='X',
            year=2019,
            transmission='автомат',
            fuel=6,
            drive_system=2,
            user=second_user
        )

        Car.objects.create(
            producer='Test Honda',
            model='CRV',
            year=2000,
            transmission='типтроник',
            fuel=1,
            drive_system=2,
            body_id=body.id,
            engine_id=engine.id,
            user=second_user
        )

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_render_cars_view_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_without_car_get_message(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['message'], 'У вас нет добавленных автомобилей')


    def test_logged_in_user_receives_all_data_on_cars(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        cars = response.context['cars']
        self.assertEqual(len(cars), 2)
        self.assertEqual(cars[0].producer, 'Test Tesla')
        self.assertEqual(cars[0].model, 'X')
        self.assertEqual(cars[0].year, 2019)
        self.assertEqual(cars[0].transmission, 'автомат')
        self.assertEqual(cars[0].fuel, 6)
        self.assertEqual(cars[0].drive_system, 2)
        self.assertEqual(cars[0].body, None)
        self.assertEqual(cars[0].engine, None)

    def test_logged_in_user_receives_name_of_car_body(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['body_name'], 'Test body name')

    def test_logged_in_user_receives_name_of_car_engine(self):
        c = Client()
        c.login(username='second-testuser', password='1234567890')
        response = c.get('/cars/')
        self.assertEqual(response.context['engine_name'], 'Test engine name')

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/cars/')
        self.assertRedirects(response, '/accounts/login/?next=/cars/', 302)


class TestCarView(TestCase):

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

        car = Car.objects.create(
            producer='Test Car with insurance, improvement, repair, car problems',
            model='X car',
            year=1999,
            transmission='автомат',
            fuel=5,
            drive_system=2,
            user=user
        )

        Car.objects.create(
            producer='Test car',
            model='CRV',
            year=2000,
            transmission='типтроник',
            fuel=9,
            drive_system=2,
            user=user
        )

        CarProblem.objects.create(
            name='Test car problem',
            description='Test description',
            state=False,
            date=date.today(),
            car_id=car.id
        )

        Insurance.objects.create(
            type='Test ОСАГО',
            policy_number='AP456789',
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
            price=599.43,
            car_id=car.id
        )

        Improvement.objects.create(
            name='Test name',
            car_id=car.id
        )

        Repair.objects.create(
            type_of_repair=2,
            name='Лобовое стекло',
            price=7699,
            date=date.today(),
            car_id=car.id
        )

        Repair.objects.create(
            type_of_repair=1,
            name='Замена масла в коробке',
            description='ATF SP-III',
            mileage=80000,
            price=1500.05,
            date=date.today(),
            car_id=car.id
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/car/2')
        self.assertRedirects(response, '/accounts/login/?next=/car/2', 302)

    def test_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='1234567890')
        self.assertTrue(logged_in)

    def test_view_return_user_name(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/2')
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_render_car_view_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/2')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_receives_car_problem_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(response.context['car_problem'][0].name, 'Test car problem')
        self.assertEqual(response.context['car_problem'][0].description, 'Test description')
        self.assertEqual(response.context['car_problem'][0].state, False)
        self.assertEqual(response.context['car_problem'][0].date, date.today())

    def test_logged_in_user_receives_insurance_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(response.context['insurance'][0].type, 'Test ОСАГО')
        self.assertEqual(response.context['insurance'][0].policy_number, 'AP456789')
        self.assertEqual(response.context['insurance'][0].start_date, date(2021, 1, 1))
        self.assertEqual(response.context['insurance'][0].end_date, date(2021, 12, 31))
        self.assertEqual(response.context['insurance'][0].price, 599.43)

    def test_logged_in_user_receives_improvement_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(response.context['improvement'][0].name, 'Test name')
        self.assertEqual(response.context['improvement'][0].state, True)
        self.assertEqual(response.context['improvement'][0].date, date.today())

    def test_logged_in_user_receives_two_repair_for_car(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/car/1')
        self.assertEqual(len(response.context['repair']), 2)


class TestAddCar(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='T',
            email='test@test.test',
            is_active=True,
            is_staff =True
        )
        user.set_password('1234567890')
        user.save()

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/add_car/')
        self.assertRedirects(response, '/accounts/login/?next=/add_car/', 302)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/add_car/')
        self.assertTemplateUsed(response, 'Garage/add_car.html')

    def test_logged_in_user_create_car_without_body_and_engine(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'CRV',
            'year': 2000,
            'transmission': 'типтроник',
            'fuel': 9,
            'drive_system': 2,
            'body': '',
            'engine': '',
            'user': user
        }
        response = c.post("/add_car/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        self.assertEqual(car.body_id, None)
        self.assertEqual(car.engine_id, None)
        self.assertRedirects(response, f'/car/{car.id}')

    def test_logged_in_user_create_car_with_body(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'Test body',
            'year': 1999,
            'transmission': 'автомат',
            'fuel': 2,
            'drive_system': 1,
            'body': 'test body name',
            'engine': '',
            'user': user
        }
        response = c.post("/add_car/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        body = Body.objects.get(name=data['body'])
        self.assertEqual(body.name, 'test body name')
        self.assertEqual(car.body_id, body.id)
        self.assertEqual(car.engine_id, None)

    def test_logged_in_user_create_car_with_engine(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'model': 'Test body',
            'year': 1999,
            'transmission': 'автомат',
            'fuel': 2,
            'drive_system': 1,
            'body': '',
            'engine': 'test engine name',
            'user': user
        }
        response = c.post("/add_car/", data=data)
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(producer=data['producer'], user_id=user.id)
        engine = Engine.objects.get(name=data['engine'])
        self.assertEqual(engine.name, 'test engine name')
        self.assertEqual(car.engine_id, engine.id)

    def test_logged_in_user_receives_error_messages(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        user = User.objects.get(username='testuser')
        data = {
            'producer': 'Test car',
            'user': user
        }
        response = c.post("/add_car/", data=data)
        self.assertEqual(Car.objects.count(), 0)
        self.assertEqual(len(response.context['errors']), 5)


class TestUpdateCar(TestCase):

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
            producer='Test update producer',
            model='Test update model',
            year=1999,
            transmission='типтроник',
            fuel=9,
            drive_system=2,
            user=user
        )

        Body.objects.create(
            name='Test body name'
        )

    def test_not_logged_in_user_redirects_to_login_page(self):
        c = Client()
        response = c.get('/update_car/1')
        self.assertRedirects(response, '/accounts/login/?next=/update_car/1', 302)

    def test_render_template_for_logged_in_user(self):
        c = Client()
        c.login(username='testuser', password='1234567890')
        response = c.get('/update_car/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Garage/update_car.html')

    def test_logged_in_user_update_year_and_body(self):
        c = Client()
        car_id = 1
        c.login(username='testuser', password='1234567890')
        response = c.get(f'/update_car/{car_id}')
        self.assertEqual(response.status_code, 200)
        car = Car.objects.get(id=car_id)
        body = Body.objects.get(name='Test body name')
        year = 2001
        form_car = CarForm(instance=car, data={'producer': car.producer, 'model': car.model, 'year': year, 'transmission': car.transmission, 'fuel': car.fuel, 'drive_system': car.drive_system})
        car.body_id = body.id
        self.assertTrue(form_car.is_valid())
        form_car.save()
        self.assertEqual(car.producer, 'Test update producer')
        self.assertEqual(car.model, 'Test update model')
        self.assertEqual(car.year, year)
        self.assertEqual(car.body_id, 1)
