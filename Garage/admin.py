from django.contrib import admin
from .models import (
    Car,
    Body,
    CarProblem,
    Engine,
    Improvement,
    Insurance,
    Repair,
)

admin.site.register(Car)
admin.site.register(Body)
admin.site.register(CarProblem)
admin.site.register(Engine)
admin.site.register(Improvement)
admin.site.register(Insurance)
admin.site.register(Repair)
