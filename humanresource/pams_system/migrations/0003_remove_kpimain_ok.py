# Generated by Django 2.2.7 on 2020-01-27 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0002_kpimain_ok'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kpimain',
            name='ok',
        ),
    ]
