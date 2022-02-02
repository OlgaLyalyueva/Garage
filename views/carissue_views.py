import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404

from Garage.models import Car, CarIssue
from Garage.forms import AddIssueForm, UpdateIssueForm
from views.views import pagination


@login_required()
def get_carissues(request):
    message = None
    user = request.user
    cars = Car.objects.filter(user_id=user.id, archive=False)
    car_issues = []
    if cars:
        for car in cars:
            if list(CarIssue.objects.filter(car_id=car.id, archive=False)) != []:
                car_issues.append(list(CarIssue.objects.filter(car_id=car.id, archive=False)))
        page_obj = pagination(request, sum(car_issues, []), 10)

        context = {
            'user': user,
            'cars': cars,
            'page_obj': page_obj,
            'message': message
        }
    else:
        message = 'У вас нет добавленных автомобилей'
        context = {
            'message': message
        }
    return render(request, 'Garage/car_issues.html', context)


@login_required()
def get_archived_issues(request):
    message = None
    issues = []
    cars = Car.objects.filter(user_id=request.user.id)
    if cars:
        for car in cars:
            if CarIssue.objects.filter(car_id=car.id, archive=True):
                issues.append(CarIssue.objects.filter(car_id=car.id, archive=True))
        if not issues:
            message = 'У вас нет добавленных поломок в папке архив'
    else:
        message = 'У вас нет добавленных автомобилей'
    context = {
        'issues': issues,
        'message': message
    }
    return render(request, 'Garage/archived_issues.html', context)


@login_required()
def add_issue(request):
    user = request.user
    cars = get_list_or_404(Car, user_id=user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_issue = AddIssueForm(request.POST)
        if form_issue.is_valid():
            form_issue.save()
            car_id = form_issue.data['car']
            return redirect(f'/car/{car_id}')
        else:
            errors = form_issue.errors

    form_issue = AddIssueForm()
    context = {
        'user': user,
        'cars': cars,
        'form_issue': form_issue,
        'errors': errors
    }
    return render(request, 'Garage/add_issue.html', context)


@login_required()
def update_issue(request, issue_id=None):
    user = request.user
    issue = get_object_or_404(CarIssue, id=issue_id, archive=False)
    car = get_object_or_404(Car, id=issue.car_id, user_id=user.id, archive=False)
    cars = Car.objects.filter(user_id=user.id, archive=False)
    errors = None
    if request.method == 'POST':
        form_issue = UpdateIssueForm(request.POST, instance=issue)
        try:
            datetime.datetime.strptime(form_issue.data['date'], "%Y-%m-%d").date()
            if form_issue.is_valid():
                form_issue.save()
                car_id = form_issue.data['car']
                return redirect(f'/car/{car_id}')
            else:
                errors = form_issue.errors
        except ValueError:
            errors = 'Дата создания поломки должна содержать день, месяц и год!'
    form_issue = UpdateIssueForm()
    context = {
        'cars': cars,
        'car': car,
        'issue': issue,
        'form_issue': form_issue,
        'errors': errors
    }
    return render(request, 'Garage/update_issue.html', context)


@login_required()
def delete_issue(request, issue_id=None):
    user = request.user
    issue = get_object_or_404(CarIssue, id=issue_id)
    car = get_object_or_404(Car, id=issue.car_id, user_id=user.id, archive=False)
    if request.method == 'POST':
        issue.delete()

        messages.add_message(
                request,
                messages.SUCCESS,
                f'Поломка была успешно удалена!'
            )
        return redirect(f'/car/{car.id}')

    context = {'issue': issue}
    return render(request, 'Garage/delete_issue.html', context)


@login_required()
def archive_issue(request, issue_id):
    user = request.user
    issue = get_object_or_404(CarIssue, id=issue_id, archive=False)
    car = get_object_or_404(Car, id=issue.car_id, user_id=user.id, archive=False)
    if request.method == 'POST':
        issue.archive = True
        issue.save()
        return redirect(f'/car/{car.id}')

    context = {
        'issue': issue
    }
    return render(request, 'Garage/archive_issue.html', context)


@login_required()
def unarchive_issue(request, issue_id=None):
    issue = get_object_or_404(CarIssue, id=issue_id, archive=True)
    if request.method == 'POST':
        issue.archive = False
        issue.save()

        return redirect(f'/car/{issue.car_id}')

    context = {
        'issue': issue
    }
    return render(request, 'Garage/unarchive_issue.html', context)
