import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Garage.models import Car, Insurance
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from Garage.forms import InsuranceForm
from views.views import pagination


@login_required()
def get_insurances(request):
    insurances = []
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    if cars:
        for car in cars:
            if list(Insurance.objects.filter(car_id=car.id, archive=False)) != []:
                insurances.append(list(Insurance.objects.filter(car_id=car.id, archive=False)))
        page_obj_insrncs = pagination(request, sum(insurances, []), 10)
        context = {
            'user': user,
            'cars': cars,
            'page_obj_insrncs': page_obj_insrncs
        }
        return render(request, 'Garage/insurances.html', context)

    else:
        message = 'У вас нет добавленных автомобилей и страховок'
        context = {
            'message': message
        }
    return render(request, 'Garage/insurances.html', context)


@login_required()
def get_archived_insurances(request):
    message = None
    insrnc = []
    context = {}
    cars = Car.objects.filter(user_id=request.user.id)
    if cars:
        for car in cars:
            if list(Insurance.objects.filter(car_id=car.id, archive=True)) != []:
                insrnc.append(list(Insurance.objects.filter(car_id=car.id, archive=True)))
        if insrnc:
            page_obj_insurances = pagination(request, sum(insrnc, []), 10)
            context['page_obj_insurances'] = page_obj_insurances
        else:
            message = 'У вас нет страховок в папке архив'
    else:
        message = 'У вас нет автомобилей и страховок'
    context['message'] = message
    return render(request, 'Garage/archived_insurances.html', context)


@login_required()
def add_insurance(request):
    user = request.user
    cars = get_list_or_404(Car, user_id=user.id, archive=False)
    context = {'user': user,
               'cars': cars
               }

    if request.method == 'POST':
        form_insrnc = InsuranceForm(request.POST)
        if form_insrnc.is_valid():
            form_insrnc.save()
            car_id = form_insrnc.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_insrnc.errors

            context['errors'] = errors
            context['form_insrnc'] = form_insrnc
            return render(request, 'Garage/add_insurance.html', context)

    form_insrnc = InsuranceForm()
    context['form_insrnc'] = form_insrnc
    return render(request, 'Garage/add_insurance.html', context)


@login_required()
def update_insurance(request, insrnc_id=None):
    user = request.user
    insrnc = get_object_or_404(Insurance, id=insrnc_id, archive=False)
    car = get_object_or_404(Car, id=insrnc.car_id, user_id=user.id, archive=False)
    cars = Car.objects.filter(user_id=user.id, archive=False)
    errors = None
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
    form_insrc = InsuranceForm()
    context = {
        'cars': cars,
        'car': car,
        'insrnc': insrnc,
        'form_insrc': form_insrc,
        'errors': errors
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
    insrnc = get_object_or_404(Insurance, id=insrnc_id, archive=False)
    car = get_object_or_404(Car, id=insrnc.car_id, user_id=user.id, archive=False)
    if request.method == 'POST':
        insrnc.archive = True
        insrnc.save()
        return redirect(f'/car/{car.id}')

    context = {
        'insrnc': insrnc
    }
    return render(request, 'Garage/archive_insurance.html', context)


@login_required()
def unarchive_insurance(request, insrnc_id=None):
    insrnc = get_object_or_404(Insurance, id=insrnc_id, archive=True)
    if request.method == 'POST':
        insrnc.archive = False
        insrnc.save()

        return redirect(f'/car/{insrnc.car_id}')

    context = {
        'insrnc': insrnc
    }
    return render(request, 'Garage/unarchive_insurance.html', context)

