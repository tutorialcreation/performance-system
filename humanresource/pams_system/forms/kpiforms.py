from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from pams_system.models.kpis import *


class KpiTypeForm(BSModalForm):
    class Meta:
        model = KpiTypes
        fields = ['maplist', 'data_to_be_assigned_kpi', 'name']


class KpiUserForm(BSModalForm):
    class Meta:
        model = KpiIndividual
        fields = ['individual']


class KpiSuspendForm(BSModalForm):
    class Meta:
        model = KpiIndividual
        fields = ['individual', 'status']


class KpiGroupForm(BSModalForm):
    class Meta:
        model = KpiGroups
        fields = ['group']


class KpiMembershipForm(BSModalForm):
    class Meta:
        model = KpiMembership
        fields = ['individual', 'group', 'effective_date_joined']


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
        model = KpiValue
        fields = ['ind', 'group', 'value']


class KpiValuesForm(BSModalForm):
    class Meta:
        model = KpiValues
        fields = ['individual', 'group', 'parent', 'value']
