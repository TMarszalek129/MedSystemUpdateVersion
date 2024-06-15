from django import forms
from . import models


YEARS = list(range(1900, 2025))

class FormLogin(forms.Form):
    login = forms.CharField(required=False, label="Login")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label='Password')

class FormChangePassword(forms.Form):
    login = forms.CharField(required=False, label="Login")
    oldpassword = forms.CharField(required=False, widget=forms.PasswordInput, label='Old Password')
    newpassword = forms.CharField(required=False, widget=forms.PasswordInput, label='New Password')

class FormPatient(forms.ModelForm):

    """
    Firstname = forms.CharField(required=True)
    Lastname = forms.CharField(required=True)
    Birthdate = forms.DateField(required=True, widget=forms.SelectDateWidget(years=YEARS))
    Login = forms.CharField(required=True)
    Password = forms.CharField(required=True, widget=forms.PasswordInput)
    """
    class Meta:
        model = models.Patient
        fields = "__all__"
        widgets = {'birthdate' : forms.SelectDateWidget(years=YEARS),
                   'password' : forms.PasswordInput
                   }

class FormMeasurement(forms.ModelForm):


    class Meta:
        model = models.Measurement
        fields = '__all__'
        widgets = {'timestamp': forms.DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'patient_id': forms.HiddenInput(attrs={'value': 0})}

    field_order = ['measure_id', 'value_a', 'value_b', 'timestamp']
"""
class MeasureUnitForm(forms.Form):
    measure_name = forms.CharField(max_length=128)
    unit_name = forms.CharField(max_length=10)
    patient_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'value': 0}))

    def save(self, commit=True):
        unit, created = models.Unit.objects.get_or_create(
            unit_name=self.cleaned_data['unit_name'],
            defaults={'patient_id_id': self.cleaned_data['patient_id']}
        )

        measure = models.Measure(
            measure_name=self.cleaned_data['measure_name'],
            unit_id=unit,
            patient_id_id=self.cleaned_data['patient_id']
        )

        if commit:
            measure.save()
        return measure
"""



class MeasureUnitForm(forms.Form):
    measure_name = forms.CharField(max_length=128)
    unit_name = forms.CharField(max_length=10)
    patient_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'value': 0}))

    def clean_measure_name(self):
        measure_name = self.cleaned_data['measure_name']
        patient_id = self.cleaned_data.get('patient_id')

        # Sprawdzenie, czy nazwa measure już istnieje dla danego pacjenta
        if models.Measure.objects.filter(measure_name=measure_name, patient_id=patient_id).exists():
            raise forms.ValidationError("Measure with this name already exists for this patient.")

        return measure_name

    def save(self, commit=True):
        # Sprawdzenie, czy pacjent istnieje
        try:
            patient = models.Patient.objects.get(id=self.cleaned_data['patient_id'])
        except models.Patient.DoesNotExist:
            raise forms.ValidationError("Patient with this ID does not exist.")

        # Pobranie lub utworzenie jednostki
        unit, created = models.Unit.objects.get_or_create(
            unit_name=self.cleaned_data['unit_name'],
            patient_id=patient
        )

        # Utworzenie measure
        measure = models.Measure(
            measure_name=self.cleaned_data['measure_name'],
            unit_id=unit,
            patient_id=patient
        )

        if commit:
            measure.save()
        return measure