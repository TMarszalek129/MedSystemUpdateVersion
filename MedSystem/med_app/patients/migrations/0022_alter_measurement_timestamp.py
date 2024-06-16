import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [

        ('patients', '0021_alter_measurement_timestamp'),

    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 15, 17, 30, 2, 265288)),
        ),
    ]
