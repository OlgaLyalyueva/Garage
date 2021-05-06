from django.urls import path
from . import view

urlpatterns = [
    path('cars/', view.cars, name='cars'),
    ]
