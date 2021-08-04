import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Garage.models import Car, Insurance
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from Garage.forms import InsuranceForm


@login_required()
def get_insurances(request):
    insurances = {}
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    if cars:
        for car in cars:
            insurances[car.id] = Insurance.objects.filter(car_id=car.id, archive=False)

        context = {
            'user': user,
            'cars': cars,
            'insurances': insurances
        }
        return render(request, 'Garage/insurances.html', context)

    else:
        message = 'У вас нет добавленных страховок'
        context = {
            'message': message
        }
    return render(request, 'Garage/insurances.html', context)


@login_required()
def add_insurance(request):
    user = request.user
    cars = get_list_or_404(Car, user_id=user.id, archive=False)
    if request.method == 'POST':
        form_insrnc = InsuranceForm(request.POST)
        if form_insrnc.is_valid():
            form_insrnc.save()
            car_id = form_insrnc.data['car']
            return redirect(f'/car/{car_id}')
        else:
            error_mes = form_insrnc.errors
            context = {
                'errors': error_mes,
                'user': user,
                'cars': cars,
            }
            return render(request, 'Garage/add_insurance.html', context)

    form_insrnc = InsuranceForm()
    context = {
        'user': user,
        'cars': cars,
        'form_insrnc': form_insrnc
    }
    return render(request, 'Garage/add_insurance.html', context)


@login_required()
def update_insurance(request, insrnc_id=None):
    user = request.user
    insrnc = get_object_or_404(Insurance, id=insrnc_id)
    car = get_object_or_404(Car, id=insrnc.car_id, user_id=user.id)
    cars = Car.objects.filter(user_id=user.id)
    if request.method == 'POST':
        form_insrnc = InsuranceForm(request.POST, instance=insrnc)
        datetime.datetime.strptime(form_insrnc.data['start_date'], "%Y-%m-%d").date()
        datetime.datetime.strptime(form_insrnc.data['end_date'], "%Y-%m-%d").date()
        if form_insrnc.is_valid():
            form_insrnc.save()
            car_id = form_insrnc.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_insrnc.errors
            context = {
                'insurance': insrnc,
                'car': car,
                'cars': cars,
                'errors': errors}
            return render(request, 'Garage/update_insurance.html', context)
    form_insrc = InsuranceForm()
    context = {
        'cars': cars,
        'car': car,
        'insrnc': insrnc,
        'form_insrc': form_insrc
    }
    return render(request, 'Garage/update_insurance.html', context)


@login_required()
def delete_insurance(request, insrnc_id=None):
    user = request.user
    insrnc = get_object_or_404(Insurance, id=insrnc_id)
    car = get_object_or_404(Car, id=insrnc.car_id, user_id=user.id, archive=False)
    if request.method == 'POST':
        insrnc.delete()

        messages.add_message(
                request,
                messages.SUCCESS,
                f'Страховой полис {insrnc.type} №{insrnc.policy_number}, был успешно удален!'
            )
        return redirect(f'/car/{car.id}')

    context = {'insurance': insrnc}
    return render(request, 'Garage/delete_insurance.html', context)


@login_required()
def archive_insurance(request, insrnc_id=None):
    user = request.user
    insrnc = get_object_or_404(Insurance, id=insrnc_id)
    car = get_object_or_404(Car, id=insrnc.car_id, user_id=user.id)
    if request.method == 'POST':
        insrnc.archive = True
        insrnc.save()
        return redirect(f'/car/{car.id}')

    context = {
        'insrnc': insrnc
    }
    return render(request, 'Garage/archive_insurance.html', context)
