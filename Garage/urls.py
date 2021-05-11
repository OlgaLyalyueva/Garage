from django.urls import path, include
from . import view

urlpatterns = [
    path('cars/', view.cars, name='cars'),
    path('car/<int:car_id>', view.car, name='car'),

    path('accounts/', include('django.contrib.auth.urls')),
    ]
