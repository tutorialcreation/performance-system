# Generated by Django 2.2.7 on 2020-02-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0014_auto_20200203_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpivalues',
            name='rank',
            field=models.FloatField(null=True),
        ),
    ]