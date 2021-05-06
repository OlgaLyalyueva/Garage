# from django.http import request, HttpResponse
from Garage.models import User, Car, Body, Engine
from django.shortcuts import render, redirect


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
        return render(request, 'cars.html', content)
    return redirect('login')


def get_name_of_body(body_id):
    body = Body.objects.get(id=body_id)
    return body.name


def get_name_of_engine(engine_id):
    engine = Engine.objects.get(id=engine_id)
    return engine.name
