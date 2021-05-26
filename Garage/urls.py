from django.urls import path, include
from django.contrib import admin

from . import view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cars/', view.get_cars, name='cars'),
    path('car/<int:car_id>', view.get_car, name='car'),
    path('add_car/', view.add_car, name='add_car'),
    path('update_car/<int:car_id>', view.update_car, name='update_car'),
    path('delete_car/<int:car_id>', view.delete_car, name='delete_car'),

    path('insurances/', view.get_insurances, name='insurances'),

    path('accounts/', include('django.contrib.auth.urls')),

    ]
