# Generated by Django 3.0.4 on 2020-03-26 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0036_auto_20190410_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='sex',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('Not Known', 'Not Known')], default='male', max_length=20, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Mss', 'Mss'), ('Dr', 'Dr'), ('Sir', 'Sir'), ('Madam', 'Madam')], default='Mr', max_length=50, null=True, verbose_name='Title'),
        ),
    ]