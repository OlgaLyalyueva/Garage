import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

from Garage.models import Car, Improvement
from Garage.forms import AddImprovementForm, UpdateImprovementForm


@login_required()
def get_improvements(request):
    improvements = {}
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    if cars:
        for car in cars:
            improvements[car.id] = list(Improvement.objects.filter(car_id=car.id, archive=False))
            if improvements[car.id] == []:
                improvements.pop(car.id)
        context = {
            'user': user,
            'cars': cars,
            'improvements': list(improvements.values())
        }
        return render(request, 'Garage/improvements.html', context)

    else:
        message = 'У вас нет добавленных автомобилей и улучшений'
        context = {
            'message': message
        }
    return render(request, 'Garage/improvements.html', context)


@login_required()
def add_improvement(request):
    user = request.user
    cars = get_list_or_404(Car, user_id=user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_impr = AddImprovementForm(request.POST)
        if form_impr.is_valid():
            form_impr.save()
            car_id = form_impr.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_impr.errors
    form_impr = AddImprovementForm()
    context = {
        'user': user,
        'cars': cars,
        'form_impr': form_impr,
        'errors': errors
    }
    return render(request, 'Garage/add_improvement.html', context)


@login_required()
def update_improvement(request, impr_id=None):
    user = request.user
    improvement = get_object_or_404(Improvement, id=impr_id, archive=False)
    car = get_object_or_404(Car, id=improvement.car_id, user_id=user.id, archive=False)
    cars = Car.objects.filter(user_id=user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_impr = UpdateImprovementForm(request.POST, instance=improvement)
        if form_impr.is_valid():
            form_impr.save()
            car_id = form_impr.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_impr.errors
    form_impr = UpdateImprovementForm()
    context = {
        'cars': cars,
        'car': car,
        'improvement': improvement,
        'form_impr': form_impr,
        'errors': errors
    }
    return render(request, 'Garage/update_improvement.html', context)
