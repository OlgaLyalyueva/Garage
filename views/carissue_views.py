from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect

from Garage.models import Car, CarIssue
from Garage.forms import IssueForm


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


@login_required()
def add_issue(request):
    user = request.user
    cars = get_list_or_404(Car, user_id=user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_issue = IssueForm(request.POST)
        if form_issue.is_valid():
            form_issue.save()
            car_id = form_issue.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_issue.errors

    form_issue = IssueForm()
    context = {
        'user': user,
        'cars': cars,
        'form_issue': form_issue,
        'errors': errors
    }
    return render(request, 'Garage/add_issue.html', context)
