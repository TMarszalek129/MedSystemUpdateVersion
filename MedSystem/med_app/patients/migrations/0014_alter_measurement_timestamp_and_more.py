# Generated by Django 5.0.6 on 2024-06-06 13:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0013_alter_measurement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 15, 54, 14, 761387)),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='value_b',
            field=models.IntegerField(default=None, null=True),
        ),
    ]