from django.urls import path, include
from django.contrib import admin

from views import car_views, insurance_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cars/', car_views.get_cars, name='cars'),
    path('car/<int:car_id>', car_views.get_car, name='car'),
    path('add_car/', car_views.add_car, name='add_car'),
    path('update_car/<int:car_id>', car_views.update_car, name='update_car'),
    path('delete_car/<int:car_id>', car_views.delete_car, name='delete_car'),

    path('insurances/', insurance_views.get_insurances, name='insurances'),

    path('accounts/', include('django.contrib.auth.urls')),

    ]
