from pams_system.tests.base_test import BaseTest
from pams_system.forms.mapforms import MapTypeForm
from pams_system.models.maps import MapType


class FormTests(BaseTest):
    
    def test_valid_form(self):
        data = {'maptype_name':'Actserv Boundary Map',
        'maptype_description':'2022',
        'status':'D'}
        form  = MapTypeForm(data = data)
        self.assertTrue(form.is_valid())