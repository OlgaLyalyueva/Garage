import datetime
from django.template.defaulttags import register

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Garage.models import Car, \
    Body, \
    Engine, \
    Insurance, \
    Repair, \
    CarIssue, \
    Improvement, \
    CarPhoto

from Garage.forms import CarForm
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from views.views import get_car_image, pagination


@login_required()
def get_cars(request):
    images = {}
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False).order_by('id')
    page_obj = pagination(request, cars, 12)
    if len(cars) > 0:
        for car in cars:
            try:
                images[car.id] = CarPhoto.objects.get(car_id=car.id).image
            except CarPhoto.DoesNotExist:
                images[car.id] = '/static/images/Garage_logo.png'
        context = {
            'images': images,
            'user': user,
            'page_obj': page_obj
        }
    else:
        message = 'У вас нет добавленных автомобилей'
        context = {
            'message': message,
            'user': user
        }
    return render(request, 'Garage/cars.html', context)


@register.filter
def get_car_id_for_image(car, id):
    return car.get(id)


@login_required()
def get_archived_cars(request):
    message = None
    cars = Car.objects.filter(user_id=request.user.id, archive=True).order_by('id')
    page_obj_cars = pagination(request, cars, 10)
    if not cars:
        message = 'У вас нет автомобилей в папке архив'
    context = {
        'user': request.user,
        'page_obj_cars': page_obj_cars,
        'message': message
    }
    return render(request, 'Garage/archived_cars.html', context)


def get_name_of_body(body_id):
    body = Body.objects.get(id=body_id)
    return body.name


def get_name_of_engine(engine_id):
    engine = Engine.objects.get(id=engine_id)
    return engine.name


@login_required
def get_car(request, car_id):
    user = request.user
    car = get_object_or_404(Car, id=car_id, user_id=user.id)
    try:
        insurances = Insurance.objects.filter(car_id=car.id, archive=False).order_by('id')
        page_obj_insurances = pagination(request, insurances, 3)
    except ObjectDoesNotExist:
        page_obj_insurances = 0

    try:
        repairs = Repair.objects.filter(car_id=car.id, archive=False).order_by('id')
        page_obj_repairs = pagination(request, repairs, 5)
    except ObjectDoesNotExist:
        page_obj_repairs = 0

    try:
        car_issues = CarIssue.objects.filter(car_id=car.id, archive=False).order_by('id')
        page_obj_car_issues = pagination(request, car_issues, 5)
    except ObjectDoesNotExist:
        page_obj_car_issues = 0

    try:
        improvements = Improvement.objects.filter(car_id=car.id, archive=False).order_by('id')
        page_obj_improvements = pagination(request, improvements, 5)
    except ObjectDoesNotExist:
        page_obj_improvements = 0

    image = get_car_image(car_id)
    context = {
        'user': user,
        'car': car,
        'page_obj_insurances': page_obj_insurances,
        'page_obj_repairs': page_obj_repairs,
        'page_obj_car_issues': page_obj_car_issues,
        'page_obj_improvements': page_obj_improvements,
        'image': image
    }
    return render(request, 'Garage/car_profile.html', context)


@login_required
def add_car(request):
    context = {}
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

            return redirect(f'/car/{car.id}')
        else:
            errors = form_car.errors
            form_car = form_car.data
            context['errors'] = errors
            context['form_car'] = form_car
            return render(request, 'Garage/add_car.html', context)

    form_car = CarForm()
    context['form_car'] = form_car
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
    car = get_object_or_404(Car, id=car_id, user_id=user.id, archive=False)
    errors = None
    now = datetime.datetime.now()
    if request.method == 'POST':
        form_car = CarForm(request.POST, instance=car)
        if form_car.is_valid():
            car = form_car.save(commit=False)
            if form_car.data['body']:
                body = add_body(form_car.data['body'])
                car.body_id = body.id
            else:
                car.body_id = None

            if form_car.data['engine']:
                engine = add_engine(form_car.data['engine'])
                car.engine_id = engine.id
            else:
                car.engine_id = None
            car.user = user
            car.save()
            return redirect(f'/car/{car.id}')
        else:
            errors = form_car.errors

    form_car = CarForm()
    image = get_car_image(car.id)
    context = {
        'user': request.user,
        'form_car': form_car,
        'car': car,
        'now': now,
        'errors': errors,
        'image': image
    }
    return render(request, 'Garage/update_car.html', context)


@login_required()
def delete_car(request, car_id=None):
    user = request.user
    car = get_object_or_404(Car, id=car_id, user_id=user.id)
    if request.method == 'POST':
        car.delete()

        messages.add_message(
                request,
                messages.SUCCESS,
                f'{car.producer} {car.model}, была успешно удалена!'
            )
        return redirect('cars')

    context = {'user': user,
               'car': car}
    return render(request, 'Garage/delete_car.html', context)


@login_required()
def archive_car(request, car_id=None):
    user = request.user
    car = get_object_or_404(Car, id=car_id, user_id=user.id, archive=False)
    if request.method == 'POST':
        car.archive = True
        car.save()

        return redirect('cars')

    context = {
        'user': user,
        'car': car
    }
    return render(request, 'Garage/archive_car.html', context)


@login_required()
def unarchive_car(request, car_id=None):
    car = get_object_or_404(Car, id=car_id, user_id=request.user.id, archive=True)
    if request.method == 'POST':
        car.archive = False
        car.save()

        return redirect(f'/car/{car.id}')

    context = {
        'user': request.user,
        'car': car
    }
    return render(request, 'Garage/unarchive_car.html', context)
