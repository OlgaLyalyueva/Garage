from django.urls import path, include
from . import view

urlpatterns = [
    path('cars/', view.cars, name='cars'),

    path('accounts/', include('django.contrib.auth.urls')),
    ]
