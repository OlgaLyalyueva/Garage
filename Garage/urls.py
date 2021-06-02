from django.urls import path, include
from django.contrib import admin

from views import car_views, insurance_views, carissue_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cars/', car_views.get_cars, name='cars'),
    path('car/<int:car_id>', car_views.get_car, name='car'),
    path('add_car/', car_views.add_car, name='add_car'),
    path('update_car/<int:car_id>', car_views.update_car, name='update_car'),
    path('delete_car/<int:car_id>', car_views.delete_car, name='delete_car'),

    path('insurances/', insurance_views.get_insurances, name='insurances'),
    path('add_insurance/', insurance_views.add_insurances, name='add_insurance'),
    path('update_insurance/<int:insrnc_id>', insurance_views.update_insurance, name='update_insurance'),
    path('delete_insurance/<int:insrnc_id>', insurance_views.delete_insurance, name='delete_insurance'),

    path('car/issues/', carissue_views.get_carissues, name='car_issues'),

    path('accounts/', include('django.contrib.auth.urls')),

    ]
