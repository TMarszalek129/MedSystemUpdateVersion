from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
import datetime
import csv
import json
import numpy as np
from . import models, forms
from django.http import Http404
from django.contrib import messages
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.core.paginator import Paginator
from django.http import HttpRequest

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
        form = forms.FormPatient(request.POST, request.FILES)
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
    patients = models.Patient.objects.all().values()
    form = forms.PatientSearchForm(request.GET)
    mess = ""

    for p in patients:
        if not p['birthdate']:
            age = 0
        else:
            patient_birth = int(p['birthdate'].strftime("%Y"))
            today = datetime.datetime.today().year
            age = today - patient_birth
        p['age'] = age


    if form.is_valid():
        lastname = form.cleaned_data.get('lastname')
        if lastname:
            patients = patients.filter(lastname__icontains=lastname)
        firstname = form.cleaned_data.get('firstname')
        if firstname:
            patients = patients.filter(firstname__icontains=firstname)
        age = form.cleaned_data.get('age')
        if age:
            patients = patients.filter(birthdate__year=today-age)
        if not patients.exists():
            patients = models.Patient.objects.all().values()
            mess = "Don't find the patient"

        items_per_page = form.cleaned_data.get('items_per_page') or 20
        go_to_page = form.cleaned_data.get('go_to_page') or 1

        for p in patients:
            if not p['birthdate']:
                age = 0
            else:
                patient_birth = int(p['birthdate'].strftime("%Y"))
                today = datetime.datetime.today().year
                age = today - patient_birth
            p['age'] = age
    else:
        items_per_page = 20
        go_to_page = None

    paginator = Paginator(patients, items_per_page + 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()

    if 'go_to_page' in query_params:
        page_obj = paginator.get_page(go_to_page)
        del query_params['go_to_page']

    if 'page' in query_params:
        del query_params['page']



    return render(request, "all_patients.html", {
        'patient': page_obj,
        'form': form,
        'mess': mess,
        'query_params': query_params.urlencode()
    })

def details(request, id):
    patient = models.Patient.objects.get(id=id)
    patient_birth = int(patient.birthdate.strftime("%Y"))
    today = datetime.datetime.today().year
    age = today - patient_birth

    weight = models.Measurement.objects.filter(patient_id=id, measure_id=1).order_by('-timestamp').values()
    height = models.Measurement.objects.filter(patient_id=id, measure_id=2).order_by('-timestamp').values()
    pulse_values = models.Measurement.objects.filter(patient_id=id, measure_id=4).order_by('-timestamp').values()
    pressure_values = models.Measurement.objects.filter(patient_id=id, measure_id=3).order_by('-timestamp').values()
    bmi = 0
    bmi_problem = False
    if (weight and height):
        weight_v = weight[0]['value_a']
        height_v = height[0]['value_a']
        bmi = round(weight_v / ((height_v / 100) * (height_v / 100)), 2)
        if (not(bmi <= 25 and bmi >= 18.5) and bmi > 0):
            bmi_problem = True


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

    heart_problem = False
    pulse_array = []
    for p in pulse_values:
        if(datetime.datetime.strptime(p['timestamp'].strftime('%Y-%m-%d'), '%Y-%m-%d') > datetime.datetime.strptime((datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), '%Y-%m-%d')):
            pulse_array.append(p['value_a'])
    if(pulse_array):
        pulse_mean = np.mean(pulse_array)
        pulse_mean = round(pulse_mean, 2)

        if (pulse_mean < pulse_down and len(pulse_array) > 3):
            heart_problem = True
        if (pulse_mean > pulse_up and len(pulse_array) > 3):
            heart_problem = True

    systonic_array, diastonic_array = [], []
    for p in pressure_values:
        if (datetime.datetime.strptime(p['timestamp'].strftime('%Y-%m-%d'), '%Y-%m-%d') > datetime.datetime.strptime(
                (datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), '%Y-%m-%d')):
            if(p['value_a'] and p['value_b']):
                systonic_array.append(p['value_a'])
                diastonic_array.append(p['value_b'])
    if (systonic_array and diastonic_array):
        syst_mean = np.mean(systonic_array)
        syst_mean = round(syst_mean, 2)

        diast_mean = np.mean(diastonic_array)
        diast_mean = round(diast_mean, 2)


        if (syst_mean < sys_pressure_down and len(systonic_array) > 3):
            heart_problem = True
        if (syst_mean > sys_pressure_up and len(systonic_array) > 3):
            heart_problem = True
        if (diast_mean < diast_pressure_down and len(diastonic_array) > 3):
            heart_problem = True
        if (diast_mean > diast_pressure_up and len(diastonic_array) > 3):
            heart_problem = True

    problems = [bmi_problem, heart_problem]

    own_measures = models.Measure.objects.filter(patient_id=id).values()
    if own_measures:
        shown = True
    else:
        shown = False

    template = loader.get_template('details.html')
    context = {
        'pt': patient,
        'age' : age,
        'shown' : json.dumps(shown),
        'problems' : json.dumps(problems)
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
    weight = models.Measurement.objects.filter(patient_id=id, measure_id=1).order_by('-timestamp').values()
    height = models.Measurement.objects.filter(patient_id=id, measure_id=2).order_by('-timestamp').values()
    pulse_values = models.Measurement.objects.filter(patient_id=id, measure_id=4).order_by('-timestamp').values()
    pressure_values = models.Measurement.objects.filter(patient_id=id, measure_id=3).order_by('-timestamp').values()


    bmi = 0
    entry = ''
    com = ''
    if(weight and height):
        weight_v = weight[0]['value_a']
        height_v = height[0]['value_a']
        bmi = round(weight_v / ( (height_v/100) * (height_v/100) ), 2)
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
    pulse_parameters = []
    pulse_com = ''
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

        if (pulse_mean < pulse_down and len(pulse_array) > 3):
            pulse_com = f"Your average pulse value is too low (standard: {pulse_down} - {pulse_up}), please visit the doctor"
        if (pulse_mean > pulse_up and len(pulse_array) > 3):
            pulse_com = f"Your average pulse value is too high (standard: {pulse_down} - {pulse_up}), please visit the doctor"

    systonic_array, diastonic_array = [], []
    syst_parameters, diast_parameters = [], []
    syst_com, diast_com = '', ''
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

def download_exams(request, id):
    exams = models.Measurement.objects.filter(patient_id=id).values()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="my_exams.csv"'},
    )

    writer = csv.writer(response, delimiter=';')
    writer.writerow(["Measure", "Value A", "Value B", "Unit", "Timestamp"])
    for m in exams:
        measure = models.Measure.objects.get(id=m['measure_id_id'])
        m['unit'] = measure.unit_id
        m['measure'] = measure.measure_name
        writer.writerow([
            m['measure'],
            m['value_a'],
            m['value_b'],
            m['unit'],
            m['timestamp']
        ])
    return response

def download_template(request, id):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="template.csv"'},
    )
    writer = csv.writer(response, delimiter=';')
    writer.writerow(["Measure", "Value A", "Value B", "Unit", "Timestamp"])
    writer.writerow(["Weight", "70", "0", "kg", "2024-06-16 12:00"])
    return response

def measurements_csv(request, id):
    if request.method == 'GET':
        form = forms.FormAddMeasurementCSV()
    else:
        form = forms.FormAddMeasurementCSV(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['file']
            fs = FileSystemStorage(location='files/')  # defaults to   MEDIA_ROOT
            filename = fs.save(file.name, file)
            try:
                with open('files/'+filename, newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                    i = 0
                    for row in spamreader:
                        i += 1
                        if (i == 1):
                            continue
                        measure = row[0]
                        measure_obj = models.Measure.objects.filter(measure_name = measure).values()
                        if not measure_obj:
                            raise
                        measure_id = measure_obj[0]['id']
                        value_a = row[1]
                        value_b = row[2]
                        unit = row[3]
                        unit_obj = models.Unit.objects.filter(unit_name=unit).values()
                        if not unit_obj:
                            raise
                        timestamp = row[4]
                        timestamp = datetime.datetime.strptime(timestamp, "%d.%m.%Y %H:%M")

                        measurement = models.Measurement(patient_id_id=id, measure_id_id=measure_id, value_a=value_a, value_b=value_b, timestamp=timestamp)
                        measurement.save()
                    commit = True
            except:
                print("Sth is wrong!")
                commit = None
            if commit is not None:
                return redirect('/patients/details/' + str(id) +'/exams')



    return render(request, "measurements_csv.html", {"f": form, "id": id})
def new_measurement(request, id):
    if request.method == 'GET':
        form = forms.FormMeasurement(patient_id=id)
    else:
        form = forms.FormMeasurement(request.POST,patient_id=id)

        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.patient_id = models.Patient.objects.get(id=id)
            measurement.save()
            return redirect('/patients/details/' + str(id))

    return render(request, "new_measurement.html", {"f": form, "id": id})

def new_measure(request, id):
    try:
        patient = models.Patient.objects.get(pk=id)
    except models.Patient.DoesNotExist:
        raise Http404("Patient does not exist")
    if request.method == 'POST':
        form = forms.MeasureUnitForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.patient_id = models.Patient.objects.get(id=id)
            form.save()
            return redirect('/patients/details/' + str(id))
    else:
        form = forms.MeasureUnitForm(initial={'patient_id': patient.id})

    return render(request, "new_measure.html", {"f": form, "id": id})

def edit_measurement(request, id, measurement_id):
    if request.method == 'GET':
        form = forms.FormMeasurement(patient_id=id)
    else:
        form = forms.FormMeasurement(request.POST,patient_id=id)
        if form.is_valid():
            measurement = models.Measurement.objects.get(id=measurement_id)
            measurement.measure_id = models.Measure.objects.get(id=request.POST['measure_id'])
            measurement.value_a = request.POST['value_a']
            measurement.value_b = request.POST['value_b']
            measurement.timestamp = request.POST['timestamp']
            measurement.save()
            return redirect('/patients/details/' + str(id) + '/exams')

    return render(request, "edit_measurement.html", {"f": form, "id": id})
def edit_measure(request, id):
    patient = get_object_or_404(models.Patient, pk=id)

    if request.method == 'POST':
        form = forms.EditMeasureUnitForm(request.POST, patient_id=patient.id)
        if form.is_valid():
            form.save(commit=False)
            form.patient_id = models.Patient.objects.get(id=id)
            form.save()
            return redirect('/patients/details/' + str(id))
    else:
        form = forms.EditMeasureUnitForm(patient_id=patient.id)

    return render(request, 'edit_measure_form.html', {'form': form, "id": id})

def del_measurement(request, id, measurement_id):

    deleted = models.Measurement.objects.get(id=measurement_id)
    deleted.delete()
    return redirect('/patients/details/' + str(id) +'/exams')

def delete_measure(request, id):
    patient = get_object_or_404(models.Patient, pk=id)
    if request.method == 'POST':
        form = forms.DeleteMeasureForm(request.POST, patient_id=patient.id)
        if form.is_valid():
            measure = form.cleaned_data['measure']
            # Usuń powiązane pomiary
            models.Measurement.objects.filter(measure_id=measure).delete()
            # Usuń powiązaną jednostkę
            unit = measure.unit_id
            measure.delete()
            # Sprawdź, czy są inne badania związane z tą jednostką
            if not models.Measure.objects.filter(unit_id=unit).exists():
                unit.delete()
            return redirect('/patients/details/' + str(id))
    else:
        form = forms.DeleteMeasureForm(patient_id=patient.id)

    return render(request, 'delete_measure.html', {'form': form, "id": id})


def select_measure_view(request,id):
    patient_id = id  # lub inna metoda na uzyskanie ID pacjenta
    if request.method == 'POST':
        form = forms.SelectMeasureForm(request.POST, patient_id=patient_id)
        if form.is_valid():
            measure = form.cleaned_data['measure']
            measurements = models.Measurement.objects.filter(measure_id=measure, patient_id=patient_id)
            if not measurements.exists() or len(measurements) == 1:
                context = {
                    'form': form,
                    'error_message': "You must first add at least two measurement for this test!",
                    "id": id,
                }
                return render(request, 'display_graphs.html', context)
            else:
                timestamps = [measurement.timestamp.strftime('%Y-%m-%d %H:%M:%S') for measurement in measurements]
                values_a = [measurement.value_a for measurement in measurements]
                values_b = [measurement.value_b for measurement in measurements if measurement.value_b > 0]
                unit = models.Unit.objects.get(unit_name=measure.unit_id)

                context = {
                    'form': form,
                    'measure': measure,
                    'timestamps': json.dumps(timestamps),
                    'values_a': json.dumps(values_a),
                    'values_b': json.dumps(values_b) if values_b else [],
                    'unit': json.dumps(unit.unit_name),
                    "id": id,
                }
                return render(request, 'display_graphs.html', context)
    else:
        form = forms.SelectMeasureForm(patient_id=patient_id)

    return render(request, 'display_graphs.html', {'form': form, "id": id})

def testing(request):
    mydata = models.Patient.objects.all().values()
    template = loader.get_template('template.html')
    context = {
        'patients': mydata,
    }
    return HttpResponse(template.render(context, request))

