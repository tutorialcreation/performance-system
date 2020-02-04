# Generated by Django 2.1.7 on 2019-03-24 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20190324_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
        migrations.AlterField(
            model_name='nationality',
            name='flag',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='religion',
            name='description',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.CharField(blank=True, max_length=125, null=True),
        ),
    ]
