from .models import Car, Body, Engine, Insurance, CarIssue
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


class IssueForm(forms.ModelForm):
    class Meta:
        model = CarIssue
        fields = ['name', 'description', 'car', 'open', 'date']
