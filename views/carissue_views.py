from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Garage.models import Car, CarIssue


@login_required()
def get_carissues(request):
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    car_issues = {}
    if cars:
        for car in cars:
            car_issues[car.id] = CarIssue.objects.filter(car_id=car.id, archive=False)

        context = {
            'user': user,
            'cars': cars,
            'car_issues': car_issues
        }
        return render(request, 'Garage/car_issues.html', context)

    else:
        message = 'У вас нет добавленных автомобилей'

    context = {
        'user': user,
        'message': message
    }
    return render(request, 'Garage/car_issues.html', context)
