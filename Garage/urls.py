from django.urls import path, include
from django.contrib import admin

from views import car_views, \
    insurance_views, \
    carissue_views, \
    improvement_views, \
    repair_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cars/', car_views.get_cars, name='cars'),
    path('cars/archived/', car_views.get_archived_cars, name='archived_cars'),
    path('car/<int:car_id>', car_views.get_car, name='car_profile'),
    path('car/add/', car_views.add_car, name='add_car'),
    path('car/update/<int:car_id>', car_views.update_car, name='update_car'),
    path('car/delete/<int:car_id>', car_views.delete_car, name='delete_car'),
    path('car/archive/<int:car_id>', car_views.archive_car, name='archive_car'),
    path('car/unarchive/<int:car_id>', car_views.unarchive_car, name='unarchive_car'),

    path('insurances/', insurance_views.get_insurances, name='insurances'),
    path('insurances/archived/', insurance_views.get_archived_insurances, name='archived_insurances'),
    path('insurance/add/', insurance_views.add_insurance, name='add_insurance'),
    path('insurance/update/<int:insrnc_id>', insurance_views.update_insurance, name='update_insurance'),
    path('insurance/delete/<int:insrnc_id>', insurance_views.delete_insurance, name='delete_insurance'),
    path('insurance/archive/<int:insrnc_id>', insurance_views.archive_insurance, name='archive_insurance'),
    path('insurance/unarchive/<int:insrnc_id>', insurance_views.unarchive_insurance, name='unarchive_insurance'),

    path('issues/', carissue_views.get_carissues, name='car_issues'),
    path('issues/archived/', carissue_views.get_archived_issues, name='archived_issues'),
    path('issue/add/', carissue_views.add_issue, name='add_issue'),
    path('issue/update/<int:issue_id>', carissue_views.update_issue, name='update_issue'),
    path('issue/delete/<int:issue_id>', carissue_views.delete_issue, name='delete_issue'),
    path('issue/archive/<int:issue_id>', carissue_views.archive_issue, name='archive_issue'),
    path('issue/unarchive/<int:issue_id>', carissue_views.unarchive_issue, name='unarchive_issue'),

    path('improvements/', improvement_views.get_improvements, name='improvements'),
    path('improvements/archived/', improvement_views.get_archived_improvements, name='archived_improvements'),
    path('improvement/add/', improvement_views.add_improvement, name='add_improvement'),
    path('improvement/update/<int:impr_id>', improvement_views.update_improvement, name='update_improvement'),
    path('improvement/delete/<int:impr_id>', improvement_views.delete_improvement, name='delete_improvement'),
    path('improvement/archive/<int:impr_id>', improvement_views.archive_improvement, name='archive_improvement'),
    path('improvement/unarchive/<int:impr_id>', improvement_views.unarchive_improvement, name='unarchive_improvement'),

    path('repairs/', repair_views.get_repairs, name='repairs'),
    path('repairs/archived/', repair_views.get_archived_repairs, name='archived_repair'),
    path('repair/add/', repair_views.add_repair, name='add_repair'),
    path('repair/update/<int:repair_id>', repair_views.update_repair, name='update_repair'),
    path('repair/delete/<int:repair_id>', repair_views.delete_repair, name='delete_repair'),
    path('repair/archive/<int:repair_id>', repair_views.archive_repair, name='archive_repair'),
    path('repair/unarchive/<int:repair_id>', repair_views.unarchive_repair, name='unarchive_repair'),

    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
