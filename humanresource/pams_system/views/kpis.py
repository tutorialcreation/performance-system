import datetime
import pandas as pd
from django.db.models import F
from django.db.models import Q, Sum, Avg, Count, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
# from django_pandas.io import read_frame

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

from pams_system.forms.kpiforms import *
from pams_system.models.maps import MapType, MapList
from pams_system.models.levels import InputData, Level
from pams_system.models.kpis import *


class KpiTypeIndex(generic.ListView):
    model = KpiTypes
    # context_object_name = 'kpi_types'
    template_name = 'kpis/index.html'

    def get_queryset(self):
        self.dataset = KpiTypes.objects.filter(
            # we will filter the maplist and level
            Q(id=int(self.kwargs['data']))  # for distinctly identifying the maplis
        )
        return KpiTypes.objects.filter(
            Q(id=self.dataset)  # filters for the maplist
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['kpi_types'] = self.dataset
        return context


class KpiTypeCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiTypeForm
    success_message = 'Success: kpitype was created.'
    success_url = reverse_lazy('kpiTypeIndex')


class KpiTypeUpdateView(BSModalUpdateView):
    model = KpiTypes
    template_name = 'kpis/update_kpi.html'
    form_class = KpiTypeForm
    success_message = 'Success: KpiType was updated.'
    success_url = reverse_lazy('kpiTypeIndex')


class KpiTypeReadView(BSModalReadView):
    model = KpiTypes
    template_name = 'kpis/read_kpi.html'


class KpiTypeDeleteView(BSModalDeleteView):
    model = KpiTypes
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Type was deleted.'
    success_url = reverse_lazy('kpiTypeIndex')


class KpiUserIndex(generic.ListView):
    model = KpiIndividual
    context_object_name = 'kpi_users'
    template_name = 'kpis/user_index.html'


class KpiUserCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiUserForm
    success_message = 'Success: Kpi User was created.'
    success_url = reverse_lazy('kpiUserIndex')

    def form_valid(self, form):
        form = super(KpiUserCreateView, self).get_form()
        if self.request.POST.get('status') == 'Y':
            form.instance.is_suspended = True
            form.instance.individual = self.request.POST.get('individual')
            form.instance.status = 'Y'
        else:
            form.instance.is_suspended = False
            form.instance.individual = self.request.POST.get('individual')
            form.instance.status = 'N'
        return super(KpiUserCreateView, self).form_valid(form)


class KpiUserUpdateView(BSModalUpdateView):
    model = KpiIndividual
    template_name = 'kpis/update_kpi.html'
    form_class = KpiSuspendForm
    success_message = 'Success: Kpi User was updated.'
    success_url = reverse_lazy('kpiUserIndex')

    def form_valid(self, form):
        form = super(KpiUserUpdateView, self).get_form()
        if self.request.POST.get('status') == 'Y':
            form.instance.is_suspended = True
            form.instance.individual = self.request.POST.get('individual')
            form.instance.status = 'Y'
        else:
            form.instance.is_suspended = False
            form.instance.individual = self.request.POST.get('individual')
            form.instance.status = 'N'
        return super(KpiUserUpdateView, self).form_valid(form)


class KpiUserReadView(BSModalReadView):
    model = KpiIndividual
    template_name = 'kpis/read_kpi.html'


class KpiUserDeleteView(BSModalDeleteView):
    model = KpiIndividual
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi User was deleted.'
    success_url = reverse_lazy('kpiUserIndex')


class KpiGroupIndex(generic.ListView):
    model = KpiGroups
    context_object_name = 'kpi_groups'
    template_name = 'kpis/group_index.html'


class KpiGroupCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiGroupForm
    success_message = 'Success: Kpi Group was created.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiGroupUpdateView(BSModalUpdateView):
    model = KpiGroups
    template_name = 'kpis/update_kpi.html'
    form_class = KpiGroupForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiMembershipView(BSModalUpdateView):
    model = KpiMembership
    template_name = 'kpis/kpi_membership.html'
    form_class = KpiMembershipForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiGroupIndex')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['membership'] = KpiMembership.objects.filter(group_id=int(self.kwargs['pk']))
        return context


def remove_member(request, individual, group):
    member = KpiIndividual.objects.get(id=individual)
    group = KpiGroups.objects.get(id=group)
    group.members.remove(member)
    return redirect('kpiGroupIndex')


class KpiGroupReadView(BSModalReadView):
    model = KpiGroups
    template_name = 'kpis/read_kpi.html'


class KpiGroupDeleteView(BSModalDeleteView):
    model = KpiGroups
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Group was deleted.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiValueIndex(generic.ListView):
    model = KpiValues
    context_object_name = 'kpi_values'
    template_name = 'kpis/value_index.html'
    # leave = get_object_or_404(Leave, id=id)
    # leave.status = 'pending'
    # leave.is_approved = False
    # leave.save()
    # messages.success(request, 'Leave is now in pending list ', extra_tags='alert alert-success alert-dismissible show')


class KpiValueCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiValuesForm
    success_message = 'Success: Kpi Value was created.'
    success_url = reverse_lazy('kpiValueIndex')


class KpiValueUpdateView(BSModalUpdateView):
    model = KpiValues
    template_name = 'kpis/update_kpi.html'
    form_class = KpiValuesForm
    success_message = 'Success: Kpi Value was updated.'
    success_url = reverse_lazy('kpiValueIndex')


class KpiValueReadView(BSModalReadView):
    model = KpiValues
    template_name = 'kpis/stats_summary.html'


class KpiStatsSummary(BSModalReadView):
    model = KpiValues
    template_name = 'kpis/stats_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.kwargs['pk'])
        context['key'] = int(self.kwargs['pk'])
        context['data'] = KpiValues.objects.filter(pk=self.kwargs['pk'])
        context['member_sum'] = KpiValues.objects.filter(pk=self.kwargs['pk']).aggregate(Sum('value'))
        context['member_average'] = KpiValues.objects.filter(pk=self.kwargs['pk']).aggregate(Avg('value'))
        context['member_ranking'] = KpiValues.objects.filter(Q(tree_id=self.kwargs['tree_id'])).annotate(
            Max('value')).order_by('-value__max')
        context['group_sum'] = KpiValues.objects.filter(
            Q(kpi_level__gte=0) & Q(tree_id=self.kwargs['tree_id'])).aggregate(Sum('value'))
        context['group_average'] = KpiValues.objects.filter(
            Q(kpi_level__gte=0) & Q(tree_id=self.kwargs['tree_id'])).aggregate(Avg('value'))
        # import pdb; pdb.set_trace()
        dataset_one = KpiValues.objects.filter(Q(kpi_level__gte=0)).aggregate(Sum('value'))
        dataset_two = KpiValues.objects.filter(Q(tree_id=self.kwargs['tree_id'])).aggregate(Sum('value'))
        group_rankings = {k: dataset_two[k] / dataset_one[k] * 100 for k in dataset_one.keys() & dataset_two}
        context['group_ranking'] = {k: dataset_two[k] / dataset_one[k] * 100 for k in dataset_one.keys() & dataset_two}
        ranks = self.model()
        ranks.rank = group_rankings['value__sum']
        # import  pdb; pdb.set_trace()
        # ranks.save()
        return context


class KpiValueDeleteView(BSModalDeleteView):
    model = KpiValues
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Value was deleted.'
    success_url = reverse_lazy('kpiValueIndex')


class KpiDatesIndex(generic.ListView):
    model = KpiDates
    context_object_name = 'kpi_dates'
    template_name = 'kpis/dates_index.html'


class KpiDatesCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiDatesForm
    success_message = 'Success: Kpi Date was created.'
    success_url = reverse_lazy('kpiDatesIndex')


class KpiDatesUpdateView(BSModalUpdateView):
    model = KpiDates
    template_name = 'kpi/update_kpi.html'
    form_class = KpiDatesForm
    success_message = 'Success: Kpi Date was updated.'
    success_url = reverse_lazy('kpiDatesIndex')


class KpiDatesReadView(BSModalReadView):
    model = KpiDates
    template_name = 'kpis/read_kpi.html'


class KpiDatesDeleteView(BSModalDeleteView):
    model = KpiDates
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Date was deleted.'
    success_url = reverse_lazy('kpiDatesIndex')


class KpiWeightsIndex(generic.ListView):
    model = KpiWeights
    context_object_name = 'kpi_weights'
    template_name = 'kpis/weight_index.html'


class KpiWeightsCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiWeightsForm
    success_message = 'Success: Kpi Weight was created.'
    success_url = reverse_lazy('kpiWeightsIndex')


class KpiWeightsUpdateView(BSModalUpdateView):
    model = KpiWeights
    template_name = 'kpis/update_kpis.html'
    form_class = KpiWeightsForm
    success_message = 'Success: Kpi Weight was updated.'
    success_url = reverse_lazy('kpiWeightsIndex')


class KpiWeightsReadView(BSModalReadView):
    model = KpiWeights
    template_name = 'kpis/read_kpi.html'


class KpiWeightsDeleteView(BSModalDeleteView):
    model = KpiWeights
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Weight was deleted.'
    success_url = reverse_lazy('kpiWeightsIndex')
