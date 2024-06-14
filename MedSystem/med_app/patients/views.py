from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import datetime
import numpy as np
from . import models, forms

def main(request):

    if request.method == 'GET':
        form = forms.FormLogin()
    else:
        form = forms.FormLogin(request.POST)


        if form.is_valid():
            login_data = request.POST['login']
            pwd_data = request.POST['password']

            try:
                patient = models.Patient.objects.get(login=login_data, password=pwd_data)
            except models.Patient.DoesNotExist:
                patient = None


            if patient is not None:
                return redirect('patients/details/' + str(patient.id))

    return render(request, 'main.html', {'f': form})

def signup(request):
    if request.method == 'GET':
        form = forms.FormPatient()
    else:
        form = forms.FormPatient(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')

    return render(request, "registration/signup.html", {"f":form})

def change_pass(request):
    if request.method == 'GET':
        form = forms.FormChangePassword()
    else:
        form = forms.FormChangePassword(request.POST)
        if form.is_valid():
            login_data = request.POST['login']
            pwd_old = request.POST['oldpassword']
            pwd_new = request.POST['newpassword']

            try:
                patient = models.Patient.objects.get(login=login_data, password=pwd_old)
                patient.password = pwd_new
                patient.save(update_fields=['password'])
            except models.Patient.DoesNotExist:
                patient = None
                print('Patient does not exists')
            if patient is not None:
                return redirect('main')

    return render(request, "registration/change_pass.html", {"f":form})


def patients(request):
    allpatients = models.Patient.objects.all().values()
    template = loader.get_template('all_patients.html')
    context = {
        'patients': allpatients,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    patient = models.Patient.objects.get(id=id)
    patient_birth = int(patient.birthdate.strftime("%Y"))
    today = datetime.datetime.today().year
    age = today - patient_birth
    template = loader.get_template('details.html')
    context = {
        'pt': patient,
        'age' : age
    }
    return HttpResponse(template.render(context, request))

def exams(request, id):
    patient = models.Patient.objects.get(id=id)
    first_name = patient.firstname
    last_name = patient.lastname
    birthday = patient.birthdate
    birthyear = int(patient.birthdate.strftime("%Y"))
    today_year = datetime.datetime.today().year
    age = today_year - birthyear
    sex = patient.sex
    sex_word = 'man' if sex == 'M' else 'woman'

    measurements = models.Measurement.objects.filter(patient_id=id).order_by('-timestamp').values()
    weight = models.Measurement.objects.filter(patient_id=id, measure_id=1).order_by('-timestamp').values()[0]['value_a']
    height = models.Measurement.objects.filter(patient_id=id, measure_id=2).order_by('-timestamp').values()[0]['value_a']
    pulse_values = models.Measurement.objects.filter(patient_id=id, measure_id=4).order_by('-timestamp').values()
    pressure_values = models.Measurement.objects.filter(patient_id=id, measure_id=3).order_by('-timestamp').values()

    bmi = 0
    entry = ''
    com = ''
    if(weight & height):
        bmi = round(weight / ( (height/100) * (height/100) ), 2)
        entry = "Your BMI based on last height and weight measurements: "
        if(bmi <= 25 and bmi >= 18.5):
            com = " -- Your weight is optimum"
        elif(bmi < 18.5):
            com = " -- Your weight is too low"
        else:
            com = " -- Your weight is too high"

    if (age <= 1):

        pulse_up = 205
        pulse_down = 105
        sys_pressure_up = 100 # systolic
        sys_pressure_down = 90
        diast_pressure_up = 60 # diastolic
        diast_pressure_down = 55

    elif (age < 11) :

        pulse_up = 140
        pulse_down = 80
        sys_pressure_up = 110
        sys_pressure_down = 100
        diast_pressure_up = 75
        diast_pressure_down = 70

    elif (age < 20):

        pulse_up = 100
        pulse_down = 60
        sys_pressure_up = 129
        sys_pressure_down = 120
        diast_pressure_up = 84
        diast_pressure_down = 80

    elif (age < 60):

        pulse_up = 80
        pulse_down = 60
        sys_pressure_up = 129
        sys_pressure_down = 120
        diast_pressure_up = 84
        diast_pressure_down = 80

    else:

        pulse_up = 70
        pulse_down = 50
        sys_pressure_up = 139
        sys_pressure_down = 130
        diast_pressure_up = 79
        diast_pressure_down = 70

    pulse_array = []
    for p in pulse_values:
        if(datetime.datetime.strptime(p['timestamp'].strftime('%Y-%m-%d'), '%Y-%m-%d') > datetime.datetime.strptime((datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), '%Y-%m-%d')):
            pulse_array.append(p['value_a'])
    if(pulse_array):
        pulse_mean = np.mean(pulse_array)
        pulse_min = np.min(pulse_array)
        pulse_max = np.max(pulse_array)
        pulse_mean = round(pulse_mean, 2)
        pulse_min = round(pulse_min, 2)
        pulse_max = round(pulse_max, 2)
        pulse_parameters = [pulse_mean, pulse_max, pulse_min]

        pulse_com = ''
        if (pulse_mean < pulse_down and len(pulse_array) > 3):
            pulse_com = f"Your average pulse value is too low (standard: {pulse_down} - {pulse_up}), please visit the doctor"
        if (pulse_mean > pulse_up and len(pulse_array) > 3):
            pulse_com = f"Your average pulse value is too high (standard: {pulse_down} - {pulse_up}), please visit the doctor"

    systonic_array, diastonic_array = [], []
    for p in pressure_values:
        if (datetime.datetime.strptime(p['timestamp'].strftime('%Y-%m-%d'), '%Y-%m-%d') > datetime.datetime.strptime(
                (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), '%Y-%m-%d')):
            if(p['value_a'] and p['value_b']):
                systonic_array.append(p['value_a'])
                diastonic_array.append(p['value_b'])
    if (systonic_array and diastonic_array):
        syst_mean = np.mean(systonic_array)
        syst_min = np.min(systonic_array)
        syst_max = np.max(systonic_array)
        syst_mean = round(syst_mean, 2)
        syst_min = round(syst_min, 2)
        syst_max = round(syst_max, 2)
        syst_parameters = [syst_mean, syst_max, syst_min]

        diast_mean = np.mean(diastonic_array)
        diast_min = np.min(diastonic_array)
        diast_max = np.max(diastonic_array)
        diast_mean = round(diast_mean, 2)
        diast_min = round(diast_min, 2)
        diast_max = round(diast_max, 2)
        diast_parameters = [diast_mean, diast_max, diast_min]

        syst_com, diast_com = '', ''
        if (syst_mean < sys_pressure_down and len(systonic_array) > 3):
            syst_com = f"Your systonic heart pressure value is too low (standard: {sys_pressure_down} - {sys_pressure_up}), please visit the doctor"
        if (syst_mean > sys_pressure_up and len(systonic_array) > 3):
            syst_com = f"Your systonic heart pressure value is too high (standard: {sys_pressure_down} - {sys_pressure_up}), please visit the doctor"
        if (diast_mean < diast_pressure_down and len(diastonic_array) > 3):
            diast_com = f"Your diastonic heart pressure value is too low (standard: {diast_pressure_down} - {diast_pressure_up}), please visit the doctor"
        if (diast_mean > diast_pressure_up and len(diastonic_array) > 3):
            diast_com = f"Your diastonic heart pressure value is too high (standard: {diast_pressure_down} - {diast_pressure_up}), please visit the doctor"

    for m in measurements:
        measure = models.Measure.objects.get(id=m['measure_id_id'])
        m['unit'] = measure.unit_id
        m['measure'] = measure.measure_name

    template = loader.get_template('exams.html')
    context = {
        'm' : measurements,
        'id' : id,
        'fname' : first_name,
        'lname' : last_name,
        'birthday' : birthday,
        'age' : age,
        'sex' : sex_word,
        'bmi' : bmi,
        'com' : com,
        'entry' : entry,
        'pulse' : pulse_parameters,
        'sys' : syst_parameters,
        'diast' : diast_parameters,
        'pcom' : pulse_com,
        'scom' : syst_com,
        'dcom' : diast_com,
    }
    return HttpResponse(template.render(context, request))
def new_measurement(request, id):
    if request.method == 'GET':
        form = forms.FormMeasurement()
    else:
        form = forms.FormMeasurement(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.patient_id = models.Patient.objects.get(id=id)
            measurement.save()
            return redirect('/patients/details/' + str(id))

    return render(request, "new_measurement.html", {"f": form, "id": id})



def testing(request):
    mydata = models.Patient.objects.all().values()
    template = loader.get_template('template.html')
    context = {
        'patients': mydata,
    }
    return HttpResponse(template.render(context, request))