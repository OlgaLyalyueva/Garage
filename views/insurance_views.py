import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Garage.models import Car, Insurance
from django.shortcuts import render, redirect, get_object_or_404
from Garage.forms import InsuranceForm


@login_required()
def get_insurances(request):
    insurances = {}
    user = request.user
    cars = Car.objects.filter(user_id=user.id)
    if cars:
        for car in cars:
            insurances[car.id] = Insurance.objects.filter(car_id=car.id)

        context = {
            'user': user,
            'cars': cars,
            'insurances': insurances
        }
        return render(request, 'Garage/insurances.html', context)
    context = {
        'user': user
    }
    return render(request, 'Garage/insurances.html', context)


@login_required()
def add_insurances(request):
    user = request.user
    cars = Car.objects.filter(user_id=user.id)
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insurances')
        else:
            error_mes = form.errors
            context = {
                'errors': error_mes,
                'user': user
            }
            return render(request, 'Garage/add_insurance.html', context)
    form = InsuranceForm()
    context = {
        'user': user,
        'cars': cars,
        'form': form
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
            return redirect('insurances')
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
        'insurance': insrnc,
        'form': form_insrc
    }
    return render(request, 'Garage/update_insurance.html', context)
