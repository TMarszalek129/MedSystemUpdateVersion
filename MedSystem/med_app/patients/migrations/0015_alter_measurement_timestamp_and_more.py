# Generated by Django 5.0.6 on 2024-06-06 13:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0014_alter_measurement_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 6, 15, 55, 15, 73349)),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='value_b',
            field=models.IntegerField(default=0, null=True),
        ),
    ]