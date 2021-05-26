from django.contrib.auth.decorators import login_required

from Garage.models import Car, Insurance
from django.shortcuts import render


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
