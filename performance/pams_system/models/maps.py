from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from pams_system.managers import SoftDeletableManager
from pams_system.managers import MapManager
# Create your models here.
'''
This is the grandfather model that contains the basic elements
which the other models will inherit. It has an abstract inheritance to the rest of them
'''


class Map(models.Model):
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
    state = models.CharField(max_length=255, choices=STATUS_CHOICES, default=NULL)
    maplist_id = models.AutoField(primary_key=True)
    # objects = models.Manager()
    # objects_delete = SoftDeletableManager()
    is_deleted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # inheritance
    class Meta:
        abstract = True

    # validations on the dates
class MapSet(models.Model):
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
    state = models.CharField(max_length=255, choices=STATUS_CHOICES, default=NULL)
    maplist_id = models.AutoField(primary_key=True)
    # objects = models.Manager()
    # objects_delete = SoftDeletableManager()
    is_deleted = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_data = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # overriding the save method in order to cater for a soft delete
    # def soft_delete(self):
    #     '''
    #     This method is removes entry from
    #     view but not from database.
    #     '''
    #     soft_delete_list = ['U', 'L', 'E', 'N']
    #     if self.status in soft_delete_list:
    #         self.is_deleted = timezone.now()
    #         self.save()

    # # overriding delete method in order to cater for a hard delete
    # def hard_delete(self):
    #     '''
    #     This method removes entry completely from
    #     the database
    #     '''
    #     hard_delete_list = ['D']
    #     if self.status in hard_delete_list:
    #         super().delete()


'''
MapType class is for simply keying in the
should not allow duplicate matype names
maptype cannot have duplicate names
'''


class MapType(Map):
    maptype_name = models.CharField(max_length=255, null=True, unique=True)
    maptype_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.maptype_name) if self.maptype_name else ''

    # validations that we need to check on the data that is streaming into the maptypes table

    # override the save method in order to prevent null maptypes
    def save(self, *args, **kwargs):
        if self.maptype_name == 'Invalid':
            return
        else:
            super().save(*args, **kwargs)


class MapList(Map):
    maptype_name = models.ForeignKey(MapType, on_delete=models.CASCADE, null=True)
    maplist_name = models.CharField(max_length=255, null=True, unique=True)
    maplist_description = models.CharField(max_length=255, null=True)
    objects = models.Manager()
    maptypes = MapManager()

    # maplist_state = models.BooleanField(null=True)

    def __str__(self):
        return str(self.maplist_name) if self.maplist_name else ''

    # # override the save method in order to prevent null maplists
    def save(self, *args, **kwargs):
        if self.maplist_name == 'Invalid':
            return
        else:
            super().save(*args, **kwargs)
