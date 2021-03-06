# Generated by Django 2.1.7 on 2019-03-25 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_auto_20190325_0151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationship',
            options={'ordering': ['created'], 'verbose_name': 'Relationship', 'verbose_name_plural': 'Relationships'},
        ),
        migrations.AddField(
            model_name='relationship',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated'),
        ),
    ]
