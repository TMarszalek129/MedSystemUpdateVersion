
# Generated by Django 5.0.6 on 2024-06-15 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [

        ('patients', '0021_alter_measurement_timestamp_alter_patient_image'),


    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 15, 17, 30, 2, 265288)),

        ),
    ]
