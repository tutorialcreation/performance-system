# Generated by Django 2.2.7 on 2020-01-28 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0003_remove_kpimain_ok'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpiweightings',
            name='historical_date',
            field=models.DateTimeField(null=True),
        ),
    ]
