# Generated by Django 3.0.4 on 2020-04-24 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0007_inputdata_previous_datastructure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputdata',
            name='previous_datastructure',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]