from .models import Car, Body, Engine, Insurance, CarIssue, Improvement, Repair, CarPhoto
from django import forms


class CarForm(forms.ModelForm):
    vin = forms.CharField(max_length=17, min_length=17, required=False)

    class Meta:
        model = Car
        fields = ['producer', 'model', 'year', 'vin', 'transmission', 'fuel', 'drive_system', 'mileage', 'price']


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

    def clean(self):
        try:
            start_date = self.cleaned_data['start_date']
            end_date = self.cleaned_data['end_date']
            if end_date <= start_date:
                raise forms.ValidationError("Дата окончания страховки должна быть позже даты начала страховки")
            return super(InsuranceForm, self).clean()
        except KeyError:
            raise forms.ValidationError("Укажите даты начала и окончания страховки")


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


class UploadCarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ['image']
