from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from pams_system.utils.fields import MultipleChoiceTreeField
from django.utils.translation import ugettext_lazy as _

from pams_system.models.kpis import *


class KpiTypeForm(BSModalForm):
    class Meta:
        model = KpiTypes
        fields = ['maplist', 'data_to_be_assigned_kpi', 'name']


# class KpiUserForm(BSModalForm):
#     class Meta:
#         model = KpiIndividual
#         fields = ['individual']

class KpiUserForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = KpiParticipants
        fields = ['maptype', 'maplist', 'individual']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['levelset'].queryset = InputData.objects.none()
    #
    #     if 'maplist' in self.data:
    #         try:
    #             maplist_id = int(self.data.get('maplist'))
    #             self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.maplist_id:
    #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)


class KpiAssignForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = KpiAssignee
        fields = [ 'kpi_assign','individual','is_suspended']

    # kpi_assign = MultipleChoiceTreeField(
    #     label=_("Assign Data Structure"),
    #     required = False,
    #     queryset= KpiAssignee.objects.all()
    # )
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.helper = FormHelper()
    #     self.helper.form_action = ""
    #     self.helper.form_method = "POST"
    #     self.helper.layout = layout.Layout(
    #         layout.Field(
    #             "kpi_assign",
    #             template="utils/checkbox_multi_select_tree.html"),
    #         bootstrap.FormActions(
    #             layout.Submit("submit", _("Save")),
    #         )
    #     )


class KpiSuspendForm(BSModalForm):
    class Meta:
        model = KpiIndividual
        fields = ['individual', 'status']


class KpiGroupForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = KpiGroupset
        fields = ['maptype', 'maplist', 'group']

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['levelset'].queryset = InputData.objects.none()
        #
        #     if 'maplist' in self.data:
        #         try:
        #             maplist_id = int(self.data.get('maplist'))
        #             self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
        #         except (ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        #     elif self.instance.maplist_id:
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)


class KpiAssignGroupForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = KpiAssignGroup
        fields = ['maptype', 'maplist', 'group']

class GroupAssignedForm(BSModalForm, forms.ModelForm):
    class Meta:
        model = KpiAssignee
        fields = ['kpi_assign', 'group']


class KpiMembershipForm(BSModalForm):
    class Meta:
        model = KpiMembers
        # fields = ['individual', 'effective_date_joined', 'group']
        fields = ['individual', 'group', 'effective_date_joined']
        #
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['levelset'].queryset = InputData.objects.none()
        #
        #     if 'maplist' in self.data:
        #         try:
        #             maplist_id = int(self.data.get('maplist'))
        #             self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
        #         except (ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        #     elif self.instance.maplist_id:
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)
        #

class KpiDatesForm(BSModalForm):
    class Meta:
        model = KpiDates
        fields = ['kpitype', 'period_date']


class KpiWeightsForm(BSModalForm):
    class Meta:
        model = KpiWeights
        fields = ['kpitype', 'maplist', 'data', 'weight']


class KpiValueForm(BSModalForm):
    class Meta:
        model = KpiValueset
        fields = ['group', 'value']

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['levelset'].queryset = InputData.objects.none()
        #     # self.fields['kpi_val'].queryset = InputData.objects.none()
        #
        #     if 'maplist' in self.data:
        #         try:
        #             maplist_id = int(self.data.get('maplist'))
        #             self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
        #         except (ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        #     elif self.instance.maplist_id:
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)


class KpiValuesForm(BSModalForm):
    class Meta:
        model = KpiValueset
        fields = ['individual', 'value']

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['levelset'].queryset = InputData.objects.none()
        #
        #     if 'maplist' in self.data:
        #         try:
        #             maplist_id = int(self.data.get('maplist'))
        #             self.fields['levelset'].queryset = Level.objects.filter(maplist_id=maplist_id)
        #         except (ValueError, TypeError):
        #             pass  # invalid input from the client; ignore and fallback to empty City queryset
        #     elif self.instance.maplist_id:
        #         self.fields['levelset'].queryset = Level.objects.filter(maplist_id=1)

#     """
#     Return a BoundField instance that will be used when accessing the form
#     field in a template.
#     """
#     return KpiValues(form, self, field_name)
