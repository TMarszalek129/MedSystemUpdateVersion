# Generated by Django 5.0.6 on 2024-06-15 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0022_alter_measurement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 15, 18, 24, 0, 323048)),
        ),
    ]
