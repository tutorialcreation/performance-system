# Generated by Django 2.2.7 on 2020-03-17 12:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0003_auto_20200317_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_date', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(blank=True, null=True), null=True, size=None)),
            ],
        ),
        migrations.AlterField(
            model_name='inputdata',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
