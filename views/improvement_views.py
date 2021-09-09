from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404

from Garage.models import Car, Improvement
from Garage.forms import AddImprovementForm


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
