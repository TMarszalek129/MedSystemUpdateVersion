from patients.models import Patient, Measurement, Measure
from faker import Faker
import numpy as np
from datetime import datetime
def generate_patients(count : int):
    fake = Faker(['pl_PL'])
    for i in range(count):
        firstname = fake.first_name()
        lastname = fake.last_name()
        birthdate = fake.date_of_birth()
        sex = np.random.choice(['M', 'W'])
        login = firstname[0] + lastname
        password = fake.password()
        patient = Patient(firstname=firstname, lastname = lastname, birthdate = birthdate, sex = sex, login = login,
                          password = password)
        patient.save()

def generate_measurements(count: int, patient_id):
    fake = Faker(['pl_PL'])
    for i in range(count):
        patient_id_instance = Patient.objects.filter(id=patient_id).values()
        measure_id = np.random.choice([1, 2, 3, 4])
        measure_id_instance = Measure.objects.filter(id=measure_id).values()
        if(measure_id == 1):
            value_a = np.random.randint(40, 140)
            value_b = 0
        elif(measure_id == 2):
            value_a = np.random.randint(150, 200)
            value_b = 0
        elif(measure_id == 3):
            value_a = np.random.randint(100, 140)
            value_b = np.random.randint(70, 90)
        else:
            value_a = np.random.randint(60, 160)
            value_b = 0
        timestamp = fake.date_time_between_dates(datetime_start=datetime(2024,1,1), datetime_end=datetime(2024,6,20))

        measurement = Measurement(patient_id_id=patient_id_instance[0]['id'], measure_id_id=measure_id_instance[0]['id'], value_a=value_a, value_b=value_b, timestamp=timestamp)
        measurement.save()


