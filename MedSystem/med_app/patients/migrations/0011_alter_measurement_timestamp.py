# Generated by Django 5.0.6 on 2024-06-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_alter_measurement_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
