from Garage.models import Car, \
    Body, \
    Engine, \
    Insurance, \
    Repair, \
    CarProblem, \
    Improvement
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

def cars(request):
    user = request.user
    if user.is_authenticated:
        cars = Car.objects.filter(user_id=user.id)
        content = {
            'cars': cars,
            'user': user.username
        }
        if len(cars) > 0:
            for car in cars:
                if car.body_id:
                    body_name = get_name_of_body(car.body_id)
                    content['body_name'] = body_name
                if car.engine_id:
                    engine_name = get_name_of_engine(car.engine_id)
                    content['engine_name'] = engine_name
        else:
            message = 'У вас нет добавленных автомобилей'
            content = {
                'message': message
            }
        return render(request, 'Garage/cars.html', content)
    return redirect('login')


def get_name_of_body(body_id):
    body = Body.objects.get(id=body_id)
    return body.name


def get_name_of_engine(engine_id):
    engine = Engine.objects.get(id=engine_id)
    return engine.name


def car(request, car_id):
    user = request.user
    if user.is_authenticated:
        car = Car.objects.get(id=car_id, user_id=user.id)
        if car:
            try:
                insurance = Insurance.objects.get(id=car.id)
            except ObjectDoesNotExist:
                insurance = None

            try:
                repair = Repair.objects.get(id=car.id)
            except ObjectDoesNotExist:
                repair = None

            try:
                car_problem = CarProblem.objects.get(id=car.id)
            except ObjectDoesNotExist:
                car_problem = None

            try:
                improvement = Improvement.objects.get(id=car.id)
            except ObjectDoesNotExist:
                improvement = None

            content = {
                'user': user,
                'car': car,
                'insurance': insurance,
                'repair': repair,
                'car_problem': car_problem,
                'improvement': improvement
            }
            return render(request, 'Garage/car.html', content)
        else:
            content = {
                'user': user
            }
            return render(request, 'Garage/add_car.html', content)
    else:
        return redirect('login')
