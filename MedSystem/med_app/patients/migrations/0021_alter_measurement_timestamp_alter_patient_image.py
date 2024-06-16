# Generated by Django 5.0.4 on 2024-06-15 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0020_patient_image_alter_measurement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 15, 17, 13, 43, 387558)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
