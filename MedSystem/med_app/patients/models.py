from django.db import models
import datetime
class Patient(models.Model):
    SEX = {
        "M": "Male",
        "F": "Female",
    }
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    birthdate = models.DateField(null=True)
    sex = models.CharField(max_length=8, choices=SEX, null=True)
    login = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Unit(models.Model):
    unit_name = models.CharField(max_length=10)
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.unit_name}"
class Measure(models.Model):
    measure_name = models.CharField(max_length=128)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT)
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.measure_name}"
class Measurement(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT)
    measure_id = models.ForeignKey(Measure, on_delete=models.PROTECT)
    value_a = models.IntegerField()
    value_b = models.IntegerField(null=True, default=0)
    timestamp = models.DateTimeField(default=datetime.datetime.now(), editable=True,)

    def __str__(self):
        return f"Measurement for {self.patient_id} - {self.measure_id}"





