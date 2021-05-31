import datetime

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
def update_insurance(request, insrc_id=None):
    user = request.user
    insrc = get_object_or_404(Insurance, id=insrc_id)
    car = get_object_or_404(Car, id=insrc.car_id, user_id=user.id)
    cars = Car.objects.filter(user_id=user.id)
    if request.method == 'POST':
        form_insrc = InsuranceForm(request.POST, instance=insrc)
        datetime.datetime.strptime(form_insrc.data['start_date'], "%Y-%m-%d").date()
        datetime.datetime.strptime(form_insrc.data['end_date'], "%Y-%m-%d").date()
        if form_insrc.is_valid():
            form_insrc.save()
            return redirect('insurances')
        else:
            errors = form_insrc.errors
            context = {
                'insurance': insrc,
                'car': car,
                'cars': cars,
                'errors': errors}
            return render(request, 'Garage/update_insurance.html', context)
    form_insrc = InsuranceForm()
    context = {
        'cars': cars,
        'car': car,
        'insurance': insrc,
        'form': form_insrc
    }
    return render(request, 'Garage/update_insurance.html', context)
