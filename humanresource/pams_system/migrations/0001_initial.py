# Generated by Django 2.2.7 on 2020-01-27 12:32

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputData',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('kpis', models.CharField(max_length=50, null=True)),
                ('weights', models.IntegerField(null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('number_of_levels', models.PositiveIntegerField(editable=False)),
                ('data_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pams_system.InputData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KpiIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KPIMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.InputData')),
            ],
        ),
        migrations.CreateModel(
            name='KpiTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapType',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('map_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_data', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_data', models.DateTimeField(auto_now_add=True, null=True)),
                ('maptype_name', models.CharField(max_length=255, null=True, unique=True)),
                ('maptype_description', models.CharField(max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapList',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('map_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_data', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_data', models.DateTimeField(auto_now_add=True, null=True)),
                ('maplist_name', models.CharField(max_length=255, null=True, unique=True)),
                ('maplist_description', models.CharField(max_length=255, null=True)),
                ('maptype_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pams_system.MapType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
                ('previous_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pams_system.Level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiWeights',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(null=True)),
                ('data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_data', to='pams_system.MapType')),
                ('kpitype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_weight', to='pams_system.KpiTypes')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_maplist', to='pams_system.MapList')),
            ],
        ),
        migrations.CreateModel(
            name='KPIWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effective_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('weight', models.IntegerField(null=True)),
                ('final_weight', models.FloatField(blank=True, null=True, verbose_name='Calculated Percentage (%) ')),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pams_system.InputData')),
            ],
        ),
        migrations.CreateModel(
            name='KpiValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True)),
                ('period_date', models.DateField(auto_now_add=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_group', to='pams_system.KpiGroups')),
                ('ind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_user', to='pams_system.KpiIndividual')),
                ('kpitype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_value', to='pams_system.KpiTypes')),
            ],
        ),
        migrations.AddField(
            model_name='kpitypes',
            name='data_to_be_assigned_kpi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType'),
        ),
        migrations.AddField(
            model_name='kpitypes',
            name='maplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList'),
        ),
        migrations.CreateModel(
            name='KpiType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('my_levels', models.PositiveIntegerField(editable=False)),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kpigroups',
            name='ind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_group', to='pams_system.KpiIndividual'),
        ),
        migrations.CreateModel(
            name='KpiDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_date', models.DateField(null=True)),
                ('kpitype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_date', to='pams_system.KpiTypes')),
            ],
        ),
        migrations.AddField(
            model_name='inputdata',
            name='kpitype',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpitypes', to='pams_system.KpiType'),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='levelset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level'),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='maplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList'),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='maptype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType'),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.InputData'),
        ),
        migrations.CreateModel(
            name='KPIWeightings',
            fields=[
                ('kpimain_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pams_system.KPIMain')),
                ('effective_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('weight', models.IntegerField(null=True)),
                ('final_weight', models.FloatField(blank=True, null=True, verbose_name='Calculated Percentage (%) ')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('kpi_levels', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KPIWeightings')),
            ],
            options={
                'abstract': False,
            },
            bases=('pams_system.kpimain', models.Model),
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]