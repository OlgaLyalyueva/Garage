from django.shortcuts import render

from Garage.models import Car, CarIssue


def get_carissues(request):
    user = request.user
    cars = Car.objects.filter(user_id=user.id)
    car_issues = {}
    if cars:
        for car in cars:
            car_issues[car.id] = CarIssue.objects.filter(car_id=car.id)
        context = {
            'user': user,
            'cars': cars,
            'car_issues': car_issues
        }
        return render(request, 'Garage/car_issues.html', context)
    context = {
        'user': user,
        'message': 'У вас нет добавленных автомобилей'
    }
    return render(request, 'Garage/car_issues.html', context)
