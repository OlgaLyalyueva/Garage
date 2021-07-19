from django.urls import path, include
from django.contrib import admin

from views import car_views, insurance_views, carissue_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cars/', car_views.get_cars, name='cars'),
    path('car/<int:car_id>', car_views.get_car, name='car_profile'),
    path('car/add', car_views.add_car, name='add_car'),
    path('car/update/<int:car_id>', car_views.update_car, name='update_car'),
    path('car/delete/<int:car_id>', car_views.delete_car, name='delete_car'),

    path('insurances/', insurance_views.get_insurances, name='insurances'),
    path('insurance/add/', insurance_views.add_insurances, name='add_insurance'),
    path('insurance/update/<int:insrnc_id>', insurance_views.update_insurance, name='update_insurance'),
    path('insurance/delete/<int:insrnc_id>', insurance_views.delete_insurance, name='delete_insurance'),

    path('issues/', carissue_views.get_carissues, name='car_issues'),

    path('accounts/', include('django.contrib.auth.urls')),

    ]
