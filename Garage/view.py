from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Garage.models import Car, \
    Body, \
    Engine, \
    Insurance, \
    Repair, \
    CarProblem, \
    Improvement
from Garage.forms import CarForm, BodyForm, EngineForm, InsuranceForm
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


@login_required()
def cars(request):
    user = request.user
    cars = Car.objects.filter(user_id=user.id)
    context = {
        'cars': cars,
        'user': user.username
    }
    if len(cars) > 0:
        for car in cars:
            if car.body_id:
                body_name = get_name_of_body(car.body_id)
                context['body_name'] = body_name
            if car.engine_id:
                engine_name = get_name_of_engine(car.engine_id)
                context['engine_name'] = engine_name
    else:
        message = 'У вас нет добавленных автомобилей'
        context = {
            'message': message
        }
    return render(request, 'Garage/cars.html', context)


def get_name_of_body(body_id):
    body = Body.objects.get(id=body_id)
    return body.name


def get_name_of_engine(engine_id):
    engine = Engine.objects.get(id=engine_id)
    return engine.name


@login_required
def car(request, car_id):
    user = request.user
    car = get_object_or_404(Car, id=car_id, user_id=user.id)
    try:
        insurance = Insurance.objects.filter(car_id=car.id)
    except ObjectDoesNotExist:
        insurance = None

    try:
        repair = Repair.objects.filter(car_id=car.id)
    except ObjectDoesNotExist:
        repair = None

    try:
        car_problem = CarProblem.objects.filter(car_id=car.id)
    except ObjectDoesNotExist:
        car_problem = None

    try:
        improvement = Improvement.objects.filter(car_id=car.id)
    except ObjectDoesNotExist:
        improvement = None

    context = {
        'user': user,
        'car': car,
        'insurance': insurance,
        'repair': repair,
        'car_problem': car_problem,
        'improvement': improvement
    }
    return render(request, 'Garage/car.html', context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form_car = CarForm(request.POST)
        if form_car.is_valid():
            car = form_car.save(commit=False)
            if form_car.data['body']:
                body = add_body(form_car.data['body'])
                car.body_id = body.id

            if form_car.data['engine']:
                engine = add_engine(form_car.data['engine'])
                car.engine_id = engine.id

            car.user = request.user
            car.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f'{car.producer} {car.model}, была успешно создана!'
            )
            return redirect(f'/car/{car.id}')
        else:
            errors = form_car.errors
            context = {'errors': errors}
            return render(request, 'Garage/add_car.html', context)
    form_car = CarForm()
    context = {
        'form_car': form_car
               }
    return render(request, 'Garage/add_car.html', context)


def add_body(body_name):
    try:
        body = Body.objects.get(name=body_name)
    except ObjectDoesNotExist:
        body = Body.objects.create(name=body_name)
    return body


def add_engine(engine_name):
    try:
        engine = Engine.objects.get(name=engine_name)
    except ObjectDoesNotExist:
        engine = Engine.objects.create(name=engine_name)
    return engine


@login_required()
def update_car(request, car_id=None):
    user = request.user
    car = get_object_or_404(Car, id=car_id, user_id=user.id)
    if request.method == 'POST':
        form_car = CarForm(request.POST, instance=car)
        if form_car.is_valid():
            car = form_car.save(commit=False)
            if form_car.data['body']:
                body = add_body(form_car.data['body'])
                car.body_id = body.id

            if form_car.data['engine']:
                engine = add_engine(form_car.data['engine'])
                car.engine_id = engine.id
            car.user = user
            car.save()

            return redirect(f'/car/{car.id}')
        else:
            errors = form_car.errors
            context = {
                'car': car,
                'errors': errors}
            return render(request, 'Garage/update_car.html', context)
    form_car = CarForm()
    context = {
        'form_car': form_car,
        'car': car
               }
    return render(request, 'Garage/update_car.html', context)
