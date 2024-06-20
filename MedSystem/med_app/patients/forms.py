from django import forms
from django.db.models import Q
from . import models
from django.db.models import Q


YEARS = list(range(1900, 2025))

class FormLogin(forms.Form):
    login = forms.CharField(required=False, label="Login", widget=forms.TextInput(attrs={'style': 'width:250px'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'style': 'width:250px'}), label='Password' )

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
        widgets = {'birthdate' : forms.SelectDateWidget(years=YEARS, attrs={'style': 'width:63px'}),
                   'password' : forms.PasswordInput,
                   'sex' : forms.Select(attrs={'style': 'width:188px'})
                   }

class FormAddMeasurementCSV(forms.Form):
    file = forms.FileField()
class FormMeasurement(forms.ModelForm):
    measure_id = forms.ModelChoiceField(queryset=models.Measure.objects.none(), label="Select Measure", widget=forms.Select(attrs={'style': 'width:200px'}))
    value_a = forms.DecimalField(max_digits=10, decimal_places=2, label="Value A", widget=forms.NumberInput(attrs={'style': 'width:200px'}))
    value_b = forms.DecimalField(max_digits=10, decimal_places=2, label="Value B", widget=forms.NumberInput(attrs={'style': 'width:200px'}))
    class Meta:
        model = models.Measurement
        fields = ['measure_id', 'value_a', 'value_b', 'timestamp', 'patient_id']
        widgets = {
            'timestamp': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'style': 'width:200px'}),
            'patient_id': forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        self.patient_id = kwargs.pop('patient_id', None)
        super(FormMeasurement, self).__init__(*args, **kwargs)
        if self.patient_id is not None:
            self.fields['measure_id'].queryset = models.Measure.objects.filter(Q(patient_id=self.patient_id) | Q(patient_id=0))
        self.fields['patient_id'].initial = self.patient_id




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


class EditMeasureUnitForm(forms.Form):
    measure = forms.ModelChoiceField(queryset=models.Measure.objects.none(), label="Select Measure to Edit", widget=forms.Select(attrs={'style': 'width:200px'}))
    measure_name = forms.CharField(max_length=128, label="New Measure Name", widget=forms.TextInput(attrs={'style': 'width:200px'}))
    unit_name = forms.CharField(max_length=10, label="New Unit Name", widget=forms.TextInput(attrs={'style': 'width:200px'}))

    def __init__(self, *args, **kwargs):
        self.patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)

        if self.patient_id is not None:
            # Filtrowanie badań przypisanych do konkretnego pacjenta
            self.fields['measure'].queryset = models.Measure.objects.filter(patient_id=self.patient_id)

        if self.data.get('measure'):
            measure = models.Measure.objects.get(pk=self.data['measure'])
            self.fields['measure_name'].initial = measure.measure_name
            self.fields['unit_name'].initial = measure.unit_id.unit_name

    def clean_measure_name(self):
        measure_name = self.cleaned_data['measure_name']
        measure_id = self.cleaned_data.get('measure').id

        # Sprawdzenie, czy nazwa measure już istnieje dla danego pacjenta, pomijając bieżący rekord
        if models.Measure.objects.filter(measure_name=measure_name, patient_id=self.patient_id).exclude(
                id=measure_id).exists():
            raise forms.ValidationError("Measure with this name already exists for this patient.")

        return measure_name

    def save(self, commit=True):
        measure = self.cleaned_data['measure']

        # Aktualizacja pola measure_name
        measure.measure_name = self.cleaned_data['measure_name']

        # Pobranie lub utworzenie jednostki
        unit, created = models.Unit.objects.get_or_create(
            unit_name=self.cleaned_data['unit_name'],
            patient_id_id=self.patient_id
        )

        # Aktualizacja pola unit_id
        measure.unit_id = unit

        if commit:
            measure.save()
        return measure

class DeleteMeasureForm(forms.Form):
    measure = forms.ModelChoiceField(
        queryset=models.Measure.objects.none(),
        label="Select Measure to Delete"
    )

    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)
        if patient_id is not None:
            self.fields['measure'].queryset = models.Measure.objects.filter(patient_id=patient_id).exclude(patient_id=0)

class SelectMeasureForm(forms.Form):
    measure = forms.ModelChoiceField(
        queryset=models.Measure.objects.none(),
        label="Select Measure"
    )

    def __init__(self, *args, **kwargs):
        self.patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)
        if self.patient_id is not None:
            self.fields['measure'].queryset = models.Measure.objects.filter(Q(patient_id=self.patient_id) | Q(patient_id=0))

class PatientSearchForm(forms.Form):
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    items_per_page = forms.IntegerField(min_value=1, initial=20, required=False, label='Items per page', widget=forms.NumberInput(attrs={'style': 'width:200px'}))
    go_to_page = forms.IntegerField(min_value=1, required=False, label='Go to this page', widget=forms.NumberInput(attrs={'style': 'width:200px'}))

