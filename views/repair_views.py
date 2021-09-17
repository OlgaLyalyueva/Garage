from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, redirect, render

from Garage.forms import RepairForm
from Garage.models import Car


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
