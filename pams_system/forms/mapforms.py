from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from pams_system.models import MapType,MapList



class MapTypeForm(BSModalForm):
    class Meta:
        model = MapType
        fields = ['maptype_name', 'maptype_description', 'status']


class MapListsForm(BSModalForm):
    class Meta:
        model = MapList
        fields = ['maptype_name', 'maplist_name', 'maplist_description']
