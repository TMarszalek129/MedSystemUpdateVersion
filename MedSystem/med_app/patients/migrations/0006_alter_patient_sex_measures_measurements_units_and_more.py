# Generated by Django 5.0.6 on 2024-06-06 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_patient_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=8, null=True),
        ),
        migrations.CreateModel(
            name='Measures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measure_name', models.CharField(max_length=128)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Measurements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_a', models.IntegerField(max_length=10)),
                ('value_b', models.IntegerField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patient')),
                ('measure_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.measures')),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=10)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patient')),
            ],
        ),
        migrations.AddField(
            model_name='measures',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.units'),
        ),
    ]