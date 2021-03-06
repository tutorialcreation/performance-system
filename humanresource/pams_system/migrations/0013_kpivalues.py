# Generated by Django 2.2.7 on 2020-02-03 07:42

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pams_system', '0012_remove_kpivalue_kpitype'),
    ]

    operations = [
        migrations.CreateModel(
            name='KpiValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True)),
                ('period_date', models.DateField(auto_now_add=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('kpi_level', models.PositiveIntegerField(editable=False)),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_individual', to='pams_system.KpiIndividual', verbose_name='Participants')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiValues', verbose_name='Group')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
