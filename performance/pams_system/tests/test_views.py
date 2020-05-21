from pams_system.tests.base_test import BaseTest
from pams_system.forms.mapforms import MapTypeForm
from pams_system.models.maps import MapType
from pams_system.views.maps import MapTypeCreateView
from django.shortcuts import reverse
from django.urls import reverse_lazy

class MapTypeCreateTest(BaseTest):
    def test_maptype_create(self):
        url = reverse_lazy("mapTypeIndex")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code,200)
