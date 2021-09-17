from .models import Car, Body, Engine, Insurance, CarIssue, Improvement, Repair
from django import forms


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['producer', 'model', 'year', 'transmission', 'fuel', 'drive_system', 'mileage', 'price']


class BodyForm(forms.ModelForm):
    class Meta:
        model = Body
        fields = ['name']


class EngineForm(forms.ModelForm):
    class Meta:
        model = Engine
        fields = ['name']


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'


class AddIssueForm(forms.ModelForm):
    class Meta:
        model = CarIssue
        fields = ['name', 'description', 'car']


class UpdateIssueForm(forms.ModelForm):
    class Meta:
        model = CarIssue
        fields = ['name', 'description', 'car', 'close', 'date']


class AddImprovementForm(forms.ModelForm):
    class Meta:
        model = Improvement
        fields = ['name', 'description', 'price', 'car']


class UpdateImprovementForm(forms.ModelForm):
    class Meta:
        model = Improvement
        fields = ['name', 'description', 'price', 'close', 'car']


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = [
            'type_of_repair',
            'name',
            'description',
            'note',
            'mileage',
            'price',
            'date',
            'car'
        ]
