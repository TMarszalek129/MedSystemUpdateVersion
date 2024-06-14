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

