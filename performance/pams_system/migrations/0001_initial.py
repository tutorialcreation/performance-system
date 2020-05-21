# Generated by Django 2.2.7 on 2020-03-17 11:44

import django.contrib.postgres.fields
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
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('kpis', models.CharField(blank=True, max_length=50, null=True)),
                ('weights', models.IntegerField(null=True)),
                ('value_date', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(blank=True, null=True), null=True, size=None)),
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
            name='KpiAssignee',
            fields=[
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=255, verbose_name='Suspend Participant')),
                ('is_suspended', models.BooleanField(default=False, help_text='button to toggle partcipant block and unblock', verbose_name='Mark Check Box below to suspend:')),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle participant deleted and undelete', verbose_name='Is Deleted')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('participant_levels', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiAssignGroup',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=128, null=True, unique=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle participant deleted and undelete', verbose_name='Is Deleted')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('group_levels', models.PositiveIntegerField(editable=False)),
                ('kpi_assign_group', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpi_group_assign', to='pams_system.InputData', verbose_name='Datastructure:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiGroupset',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(max_length=128, null=True, unique=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle participant deleted and undelete', verbose_name='Is Deleted')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('group_levels', models.PositiveIntegerField(editable=False)),
                ('kpi_group', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpi_groups', to='pams_system.InputData', verbose_name='Datastructure:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=255, verbose_name='Suspend Participant')),
                ('individual', models.CharField(max_length=200, null=True)),
                ('is_suspended', models.BooleanField(default=False, help_text='button to toggle partcipant block and unblock', verbose_name='Is Blocked')),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle participant deleted and undelete', verbose_name='Is Deleted')),
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
            name='KpiStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_str', models.CharField(blank=True, max_length=200, null=True)),
                ('kpis', models.CharField(blank=True, max_length=200, null=True)),
                ('weights', models.FloatField(null=True)),
                ('value', models.IntegerField(null=True)),
                ('individual', models.CharField(blank=True, max_length=200, null=True)),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
                ('value_date', models.DateField(null=True)),
                ('contribution_to_performance', models.FloatField(null=True)),
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
                ('state', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('maplist_id', models.AutoField(primary_key=True, serialize=False)),
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
                ('state', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('maplist_id', models.AutoField(primary_key=True, serialize=False)),
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
            name='KpiValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True)),
                ('rank', models.FloatField(null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_groupset', to='pams_system.KpiGroupset')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_individual', to='pams_system.KpiIndividual', verbose_name='Participants')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiValues', verbose_name='Categories')),
                ('value_date', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inputs', to='pams_system.InputData')),
            ],
        ),
        migrations.CreateModel(
            name='KpiValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True)),
                ('period_date', models.DateField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_groups', to='pams_system.KpiGroupset')),
                ('ind', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_user', to='pams_system.KpiIndividual')),
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
        migrations.CreateModel(
            name='KpiParticipants',
            fields=[
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=255, verbose_name='Suspend Participant')),
                ('individual', models.CharField(max_length=200, null=True)),
                ('is_suspended', models.BooleanField(default=False, help_text='button to toggle partcipant block and unblock', verbose_name='Is Blocked')),
                ('is_deleted', models.BooleanField(default=False, help_text='button to toggle participant deleted and undelete', verbose_name='Is Deleted')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('participant_levels', models.PositiveIntegerField(editable=False)),
                ('kpi_ind', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpi_individuals', to='pams_system.InputData', verbose_name='Datastructure:')),
                ('levelset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiParticipants')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KpiMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effective_date_joined', models.DateField(null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pams_system.KpiAssignGroup')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pams_system.KpiAssignee')),
            ],
        ),
        migrations.CreateModel(
            name='KpiMembers',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('effective_date_joined', models.DateField(null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pams_system.KpiGroupset')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pams_system.KpiParticipants')),
                ('levelset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kpigroupset',
            name='levelset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level'),
        ),
        migrations.AddField(
            model_name='kpigroupset',
            name='maplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList'),
        ),
        migrations.AddField(
            model_name='kpigroupset',
            name='maptype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType'),
        ),
        migrations.AddField(
            model_name='kpigroupset',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiGroupset'),
        ),
        migrations.CreateModel(
            name='KpiDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_date', models.DateField(null=True)),
                ('kpitype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_date', to='pams_system.KpiTypes')),
            ],
        ),
        migrations.CreateModel(
            name='KpiData',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('kpis', models.CharField(max_length=50, null=True)),
                ('weights', models.IntegerField(null=True)),
                ('value_date', models.DateTimeField(blank=True, null=True, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('kpi_levels', models.PositiveIntegerField(editable=False)),
                ('kpitypes', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpitypeset', to='pams_system.InputData', verbose_name='Datastructure:')),
                ('levelset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kpiassigngroup',
            name='levelset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_level', to='pams_system.Level'),
        ),
        migrations.AddField(
            model_name='kpiassigngroup',
            name='maplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList'),
        ),
        migrations.AddField(
            model_name='kpiassigngroup',
            name='maptype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType'),
        ),
        migrations.AddField(
            model_name='kpiassigngroup',
            name='members',
            field=models.ManyToManyField(through='pams_system.KpiMembership', to='pams_system.KpiAssignee'),
        ),
        migrations.AddField(
            model_name='kpiassigngroup',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiAssignGroup'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.KpiGroupset'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.KpiParticipants'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='kpi_assign',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpi_assign', to='pams_system.InputData', verbose_name='Datastructure:'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='maplist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='maptype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType'),
        ),
        migrations.AddField(
            model_name='kpiassignee',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiAssignee'),
        ),
        migrations.CreateModel(
            name='InputDatas',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('kpis', models.CharField(max_length=50, null=True)),
                ('weights', models.IntegerField(null=True)),
                ('value_date', models.DateField(null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('number_of_levels', models.PositiveIntegerField(editable=False)),
                ('data_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pams_system.InputDatas')),
                ('kpitype', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kpitypeset', to='pams_system.KpiType')),
                ('levelset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='pams_system.InputDatas')),
            ],
            options={
                'abstract': False,
            },
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
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.InputData', verbose_name='Data Structure'),
        ),
        migrations.CreateModel(
            name='KPIWeightings',
            fields=[
                ('kpimain_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pams_system.KPIMain')),
                ('effective_date', models.DateField(null=True)),
                ('historical_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('weight', models.IntegerField(null=True)),
                ('kpis', models.CharField(blank=True, max_length=200, null=True)),
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
        migrations.CreateModel(
            name='KpiValueset',
            fields=[
                ('status', models.CharField(choices=[('U', 'Unlocked'), ('L', 'Locked'), ('E', 'Edited'), ('D', 'Deleted'), ('N', 'Null')], default='N', max_length=255)),
                ('main_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_deleted', models.DateTimeField(auto_now_add=True, null=True)),
                ('indicator', models.BooleanField(default=False)),
                ('value', models.FloatField(null=True)),
                ('value_dates', models.DateField(blank=True, null=True)),
                ('rank', models.FloatField(null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('kpi_level', models.PositiveIntegerField(editable=False)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_group_val', to='pams_system.KpiGroupset')),
                ('individual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_ind_val', to='pams_system.KpiParticipants', verbose_name='Participants')),
                ('kpi_val', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kpi_val', to='pams_system.InputData')),
                ('levelset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.Level')),
                ('maplist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapList')),
                ('maptype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pams_system.MapType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pams_system.KpiValueset', verbose_name='Categories')),
                ('kpi_weight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weightings', to='pams_system.KPIWeightings')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
