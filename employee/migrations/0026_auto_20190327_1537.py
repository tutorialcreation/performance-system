# Generated by Django 2.1.7 on 2019-03-27 15:37

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0025_auto_20190327_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergency',
            name='tel',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+233240000000', help_text='Enter number with Country Code Eg. +233240000000', max_length=128, verbose_name='Phone Number (Example +233240000000)'),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='tel',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+233240000000', help_text='Enter number with Country Code Eg. +233240000000', max_length=128, verbose_name='Phone Number (Example +233240000000)'),
        ),
    ]
