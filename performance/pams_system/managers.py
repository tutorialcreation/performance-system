from django.db import models
from django.utils import timezone
from django.db.models import Q

class SoftDeletableQs(models.QuerySet):
    '''
    This query allows for soft  - deletion
    on their objects
    '''

    def delete(self, **kwargs):
        self.update(is_deleted=timezone.now(), **kwargs)

    '''
    And this will perform a hard delete
    '''

    def hard_delete(self, **kwargs):
        super().delete(**kwargs)


class SoftDeletableManager(models.Manager):
    '''
    This manager filters out the soft deleted objects
    '''

    def get_queryset(self):
        return SoftDeletableQs(
            model=self.model, using=self.db, hints=self._hints
        ).filter(
            is_deleted__isnull=True
        )


class MapQueryset(models.QuerySet):
    def get_maptypes(self, *args, **kwargs):
        self.maptype_name = self.model.objects.filter(
            # we will filter the maplist and level
            Q(maptype_name_id__maptype_name=self.model.maptype_name)  # for distinctly identifying the maptypes
        )
        return self.model.objects.filter(
            Q(maptype_name_id__maptype_name=self.maptype_name)  # filters for the maptypes
        )


class MapManager(models.Manager):
    def get_queryset(self):
        return MapQueryset(self.model, using=self._db)

    def get_maptypes(self, *args, **kwargs):
        return self.get_queryset().get_maptypes()


class LevelQuerysets(models.QuerySet):

    def get_levels(self, *args, **kwargs):
        self.maplist = self.model.objects.filter(
            # we will filter the maplist and level
            Q(maplist_id__maplist_name=self.kwargs['maplist'])  # for distinctly identifying the maplis
        )
        return self.model.objects.filter(
            Q(maplist_id__maplist_name=self.maplist)  # filters for the maplist
        )


class LevelManager(models.Manager):
    def levels(self, *args, **kwargs):
        return self.get_queryset().get_levels()
