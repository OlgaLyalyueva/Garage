from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, redirect, render

from Garage.forms import RepairForm
from Garage.models import Repair, Car


@login_required()
def get_repairs(request):
    repairs = {}
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    if cars:
        for car in cars:
            repairs[car.id] = list(Repair.objects.filter(car_id=car.id, archive=False))
            if repairs[car.id] == []:
                repairs.pop(car.id)
        context = {
            'user': user,
            'cars': cars,
            'repairs': list(repairs.values())
        }
        return render(request, 'Garage/repairs.html', context)

    else:
        message = 'У вас нет добавленных автомобилей и ремонтов'
        context = {
            'message': message
        }
    return render(request, 'Garage/repairs.html', context)


@login_required
def add_repair(request):
    cars = get_list_or_404(Car, user_id=request.user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_repair = RepairForm(request.POST)
        if form_repair.is_valid():
            form_repair.save()
            car_id = form_repair.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_repair.errors

    form_repair = RepairForm()
    context = {
        'user': request.user,
        'cars': cars,
        'form_repair': form_repair,
        'errors': errors
    }
    return render(request, 'Garage/add_repair.html', context)
