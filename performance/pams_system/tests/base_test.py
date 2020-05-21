from django.test import TestCase
import unittest
from pams_system.models.maps import MapSet,MapType

class BaseTest(TestCase):

    def create_map(self):
        map = MapSet.objects.create(status='N',state='D')
        return map

    

    def create_maptype(self):
        maptype = MapType.objects.create(maplist_id=3,state='D',status='N',
        maptype_name='Actserv Boundary Map', maptype_description='2022')
        return maptype
