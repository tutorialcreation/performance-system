from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import F
from django.forms import Textarea

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from pams_system.models.levels import InputData, Level, KPIWeight, KPIWeightings
from pams_system.models.maps import MapList, MapType


class LevelStructureForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = InputData
        fields = ['maptype', 'maplist', 'levelset', 'name', 'parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['levelset'].queryset = InputData.objects.none()

        if 'maplist' in self.data:
            try:
                maplist_id = int(self.data.get('maplist'))
                self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.maplist_id:
            self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)


class LevelListForm(BSModalForm):
    class Meta:
        model = Level
        fields = ['maptype', 'maplist', 'previous_level', 'name']


class LevelTypeForm(BSModalForm):
    class Meta:
        model = InputData
        fields = ['data_name']


class KPIWeightForm(forms.ModelForm):
    class Meta:
        model = KPIWeightings
        fields = ['effective_date','content', 'weight']
    # def __init__(self, *args, **kwargs):
    #     super(KPIWeightForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance:
    #         self.fields['final_weight'].required = False
    #         self.fields['final_weight'].widget.attrs['readonly'] = True
