from django.db import models
from django.urls import reverse
from django.utils import timezone
# from pams_system.models.kpis import KpiTypes
from mptt.models import MPTTModel, TreeForeignKey
from pams_system.models.maps import MapList, MapType
from django.contrib.postgres.fields import ArrayField
from pams_system.managers import SoftDeletableManager, LevelManager

'''
This model is the grandfather model for the 
rest of the models and classes through abstract inheritance.
'''


class MainLevel(models.Model):
    UNLOCKED = 'U'
    LOCKED = 'L'
    EDITED = 'E'
    DELETED = 'D'
    NULL = 'N'
    STATUS_CHOICES = (
        (UNLOCKED, 'Unlocked'),
        (LOCKED, 'Locked'),
        (EDITED, 'Edited'),
        (DELETED, 'Deleted'),
        (NULL, 'Null'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=NULL)
    # date_state = models.BooleanField(null=True, default=False)
    # objects = models.Manager()
    main_id = models.AutoField(primary_key=True)
    # objects_delete = SoftDeletableManager()
    is_deleted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    maptype = models.ForeignKey(MapType, on_delete=models.SET_NULL, null=True)
    maplist = models.ForeignKey(MapList, on_delete=models.SET_NULL, null=True)

    # inheritance
    class Meta:
        abstract = True

    # validations on the dates

    # overriding the save method in order to cater for a soft delete
    def soft_delete(self):
        '''
        This method is removes entry from
        view but not from database.
        '''
        soft_delete_list = ['U', 'L', 'E', 'N']
        if self.status in soft_delete_list:
            self.is_deleted = timezone.now()
            self.save()

    # overriding delete method in order to cater for a hard delete
    def hard_delete(self):
        '''
        This method removes entry completely from
        the database
        '''
        hard_delete_list = ['D']
        if self.status in hard_delete_list:
            super().delete()


class MainKpis(models.Model):
    maplist = models.ForeignKey(MapList, on_delete=models.SET_NULL, null=True)

    # kpi_id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Level(MainLevel):
    name = models.CharField(max_length=255, null=True)
    previous_level = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class KpiType(MainKpis, MPTTModel):
    name = models.CharField(max_length=200, null=True)
    # data_to_be_assigned_kpi = models.ForeignKey(InputData, on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'my_levels'
        order_insertion_by = ['name']


class InputData(MainLevel, MPTTModel):
    name = models.CharField(max_length=50, unique=False, null=True)
    kpis = models.CharField(max_length=50, unique=False, null=True)
    data_name = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    kpitype = TreeForeignKey(KpiType, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='kpitypes')
    weights = models.IntegerField(null=True)
    value_date = ArrayField(models.DateTimeField(), null=True)

    # multiple_dates = ArrayField(models.DateTimeField(),null=True)
    # multiple_dates = models.DateTimeField(null=True, blank=True)

    #
    # date_status = models.BooleanField(null=True,default=False)
    # state_of_dates = models.BooleanField(null=True,default=False)
    # objects = models.Manager()
    # get_levels = LevelManager()

    def __str__(self):
        import datetime
        return '{}'.format(self.name)
        # return self.value_date.strftime("%Y,%d,%m") if self.value_date else '2019-2-1'

    class MPTTMeta:
        level_attr = 'number_of_levels'
        order_insertion_by = ['name', 'kpis']


class InputDatas(MainLevel, MPTTModel):
    name = models.CharField(max_length=50, unique=False, null=True)
    kpis = models.CharField(max_length=50, unique=False, null=True)
    data_name = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='childs')
    kpitype = TreeForeignKey(KpiType, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='kpitypeset')
    weights = models.IntegerField(null=True)
    value_date = ArrayField(ArrayField(models.DateTimeField(), size=20), size=20)
    # multiple_dates = ArrayField(models.DateTimeField(null=True), blank=True)

    # multiple_dates = models.DateTimeField(null=True, blank=True)

    #
    # date_status = models.BooleanField(null=True,default=False)
    # state_of_dates = models.BooleanField(null=True,default=False)
    # objects = models.Manager()
    # get_levels = LevelManager()

    def __str__(self):
        import datetime
        return '{}'.format(self.name)
        # return self.value_date.strftime("%Y,%d,%m") if self.value_date else '2019-2-1'

    class MPTTMeta:
        level_attr = 'number_of_levels'
        order_insertion_by = ['name', 'kpis']


class KpiData(MainLevel, MPTTModel):
    name = models.CharField(max_length=50, unique=False, null=True)
    kpis = models.CharField(max_length=50, unique=False, null=True)
    levelset = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    kpitypes = TreeForeignKey(InputData, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='kpitypeset', verbose_name='Datastructure:')
    weights = models.IntegerField(null=True)
    value_date = models.DateTimeField(null=True, blank=True, unique=True)

    # objects = models.Manager()
    # get_levels = LevelManager()

    def __str__(self):
        import datetime
        return self.name
        # return self.value_date.strftime("%Y,%d,%m") if self.value_date else '2019-2-1'

    class MPTTMeta:
        level_attr = 'kpi_levels'
        order_insertion_by = ['name', 'kpis']


class KPIMain(models.Model):
    content = models.ForeignKey(InputData, on_delete=models.SET_NULL, null=True)
    # ok = models.IntegerField(null=True)
    # kpimain_ptr_id = models.AutoField(primary_key=True, default=1)

    # class Meta:
    # abstract = True


class KPIWeight(models.Model):
    effective_date = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    content = models.ForeignKey(InputData, on_delete=models.CASCADE, null=True)
    weight = models.IntegerField(null=True)
    final_weight = models.FloatField("Calculated Percentage (%) ", null=True, blank=True)

    def __float__(self):
        return self.weight


class KPIWeightings(KPIMain, MPTTModel):
    effective_date = models.DateField(auto_now_add=False, null=True)
    historical_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    weight = models.IntegerField(null=True)
    final_weight = models.FloatField("Calculated Percentage (%) ", null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    def __float__(self):
        return self.weight

    class MPTTMeta:
        level_attr = 'kpi_levels'
        order_insertion_by = ['weight']
