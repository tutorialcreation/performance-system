# Generated by Django 2.2.7 on 2020-01-28 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0004_kpiweightings_historical_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpiweightings',
            name='effective_date',
            field=models.DateField(null=True),
        ),
    ]
