from django.db import models
from pams_system.models.maps import MapList, MapType
from pams_system.models.levels import InputData, MainLevel, Level
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _


class MainKpis(models.Model):
    maplist = models.ForeignKey(MapList, on_delete=models.SET_NULL, null=True)

    # kpi_id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class KpiTypes(MainKpis):
    name = models.CharField(max_length=200, null=True)
    data_to_be_assigned_kpi = models.ForeignKey(MapType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# class KpiType(MainKpis, MPTTModel):
#     name = models.CharField(max_length=200, null=True)
#     data_to_be_assigned_kpi = models.ForeignKey(InputData, on_delete=models.SET_NULL, null=True)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
#                             related_name='children')
#
#     def __str__(self):
#         return self.name
#
#     class MPTTMeta:
#         level_attr = 'my_levels'
#         order_insertion_by = ['name'parent',']


class KpiIndividual(models.Model):
    YES = 'Y'
    NO = 'N'
    STATUS_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )
    status = models.CharField('Suspend Participant', max_length=255, choices=STATUS_CHOICES, default=NO)
    individual = models.CharField(max_length=200, null=True)
    is_suspended = models.BooleanField(_('Is Blocked'), help_text='button to toggle partcipant block and unblock',
                                       default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle participant deleted and undelete',
                                     default=False)

    def __str__(self):
        return self.individual

    class MPTTMeta:
        level_attr = 'kpi_levels'
        order_insertion_by = ['name', 'kpis']


class KpiParticipants(MainLevel, MPTTModel):
    YES = 'Y'
    NO = 'N'
    STATUS_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )
    status = models.CharField('Suspend Participant', max_length=255, choices=STATUS_CHOICES, default=NO)
    individual = models.CharField(max_length=200, null=True)
    is_suspended = models.BooleanField(_('Is Blocked'), help_text='button to toggle partcipant block and unblock',
                                       default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle participant deleted and undelete',
                                     default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    kpi_ind = TreeForeignKey(InputData, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='kpi_individuals', verbose_name='Datastructure:')

    def __str__(self):
        return self.individual

    class MPTTMeta:
        level_attr = 'participant_levels'
        order_insertion_by = ['individual']


class KpiAssignee(MainLevel, MPTTModel):
    YES = 'Y'
    NO = 'N'
    STATUS_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )
    status = models.CharField('Suspend Participant', max_length=255, choices=STATUS_CHOICES, default=NO)
    individual = models.CharField(max_length=200, null=True)
    is_suspended = models.BooleanField(_('Is Blocked'), help_text='button to toggle partcipant block and unblock',
                                       default=False)
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle participant deleted and undelete',
                                     default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    # levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    kpi_assign = TreeForeignKey(InputData, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='kpi_assign', verbose_name='Datastructure:')

    def __str__(self):
        return self.individual

    class MPTTMeta:
        level_attr = 'participant_levels'
        order_insertion_by = ['individual']

class KpiGroupset(MainLevel, MPTTModel):
    group = models.CharField(max_length=128, null=True, unique=True)
    # members = models.ManyToManyField(KpiParticipants, through='KpiMembership')
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle participant deleted and undelete',
                                     default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    kpi_group = TreeForeignKey(InputData, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='kpi_groups', verbose_name='Datastructure:')

    # main_id = models.OneToOneField()

    def __str__(self):
        return self.group

    class MPTTMeta:
        level_attr = 'group_levels'
        order_insertion_by = ['group']



class KpiAssignGroup(MainLevel, MPTTModel):
    group = models.CharField(max_length=128, null=True, unique=True)
    members = models.ManyToManyField(KpiAssignee, through='KpiMembership')
    is_deleted = models.BooleanField(_('Is Deleted'), help_text='button to toggle participant deleted and undelete',
                                     default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True, related_name="group_level")
    kpi_assign_group = TreeForeignKey(InputData, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='kpi_group_assign', verbose_name='Datastructure:')

    # main_id = models.OneToOneField()

    def __str__(self):
        return self.group

    class MPTTMeta:
        level_attr = 'group_levels'
        order_insertion_by = ['group']

#
# class KpiGroups(models.Model):
#     group = models.CharField(max_length=128, null=True, unique=True)
#     members = models.ManyToManyField(KpiParticipants, through='KpiMembership')
#
#     def __str__(self):
#         return self.group


class KpiMembership(models.Model):  # intermediate model
    individual = models.ForeignKey(KpiAssignee, on_delete=models.CASCADE)  # source models
    group = models.ForeignKey(KpiAssignGroup, on_delete=models.CASCADE)  # source models
    # effective_date_joined = models.ForeignKey(InputData, on_delete=models.CASCADE, to_field="value_date",
    # blank=True, null=True)
    effective_date_joined = models.DateField(null=True)
    # main_id = models.OneToOneField(KpiGroupset, on_delete=models.CASCADE, parent_link=True, related_name='kpi_member_main')

class KpiMembers(MainLevel,models.Model):  # intermediate model
    individual = models.ForeignKey(KpiParticipants, on_delete=models.CASCADE)  # source models
    group = models.ForeignKey(KpiGroupset, on_delete=models.CASCADE)  # source models
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    # effective_date_joined = models.ForeignKey(InputData, on_delete=models.CASCADE, to_field="value_date",
    # blank=True, null=True)
    effective_date_joined = models.DateField(null=True)
    # main_id = models.OneToOneField(KpiGroupset, on_delete=models.CASCADE, parent_link=True, related_name='kpi_member_main')


class KpiDates(models.Model):
    kpitype = models.ForeignKey(KpiTypes, on_delete=models.SET_NULL, related_name='kpi_date', null=True)
    period_date = models.DateField(null=True)

    def __str__(self):
        return self.period_date


class KpiWeights(models.Model):
    kpitype = models.ForeignKey(KpiTypes, on_delete=models.SET_NULL, related_name='kpi_weight', null=True)
    maplist = models.ForeignKey(MapList, on_delete=models.SET_NULL, related_name='kpi_maplist', null=True)
    data = models.ForeignKey(MapType, on_delete=models.SET_NULL, related_name='kpi_data', null=True, blank=True)
    weight = models.FloatField(null=True)

    def __float__(self):
        return self.weight


class KpiValue(models.Model):
    ind = models.ForeignKey(KpiIndividual, on_delete=models.SET_NULL, related_name='kpi_user', null=True, blank=True)
    group = models.ForeignKey(KpiGroupset, on_delete=models.SET_NULL, related_name='kpi_groups', null=True, blank=True)
    indicator = models.BooleanField(default=False)
    value = models.FloatField(null=True)
    period_date = models.DateField(auto_now_add=False, null=True, blank=True)


class KpiValueMain(models.Model):
    indicator = models.BooleanField(default=False)

    class Meta:
        abstract = True


class KpiValues(models.Model):
    individual = models.ForeignKey(KpiIndividual, on_delete=models.SET_NULL, related_name='kpi_individual',
                                   verbose_name='Participants', null=True, blank=True)
    group = models.ForeignKey(KpiGroupset, on_delete=models.SET_NULL, related_name='kpi_groupset', null=True,
                              blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Categories')
    indicator = models.BooleanField(default=False)
    value = models.FloatField(null=True)
    value_date = models.ForeignKey(InputData, on_delete=models.SET_NULL, null=True, blank=True, related_name="inputs")
    value_dates = models.DateField(null=True, blank=True)
    rank = models.FloatField(null=True)

    def __str__(self):
        return self.individual.individual


class KpiValueset(MainLevel, MPTTModel):
    individual = models.ForeignKey(KpiIndividual, on_delete=models.SET_NULL, related_name='kpi_ind_val',
                                   verbose_name='Participants', null=True, blank=True)
    group = models.ForeignKey(KpiGroupset, on_delete=models.SET_NULL, related_name='kpi_group_val', null=True,
                              blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Categories')
    indicator = models.BooleanField(default=False)
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.FloatField(null=True)
    kpi_val = models.ForeignKey(InputData, on_delete=models.SET_NULL, null=True, blank=True, related_name="kpi_val")
    value_dates = models.DateField(null=True, blank=True)
    rank = models.FloatField(null=True)

    def __str__(self):
        return self.individual.individual

    class MPTTMeta:
        level_attr = 'kpi_level'
        order_insertion_by = ['individual']
