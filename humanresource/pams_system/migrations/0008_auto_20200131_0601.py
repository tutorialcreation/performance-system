# Generated by Django 2.2.7 on 2020-01-31 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0007_auto_20200131_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpigroups',
            name='group',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
