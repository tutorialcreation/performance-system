import os, sys
import datetime
from datetime import timedelta,date,datetime
import time
import calendar
# from datetime import date,datetime
# import datetime
import pandas as pd
import itertools
from django.db.models import Q, F, Sum, Avg, Count, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
import io
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)
from pams_system.forms.kpiforms import *
from pams_system.models.maps import MapType, MapList
from pams_system.models.levels import InputData, Level
from pams_system.models.kpis import *
from django.db import connection
from pams_system.utils.search_algorithms import get_value_dates, get_weights, get_kpis,lastdayofmonth
from pams_system.filters import ValueFilter
# from weasyprint import HTML

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
    model = KpiParticipants
    context_object_name = 'kpi_users'
    template_name = 'kpis/user_index.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        participant_list = KpiParticipants.objects.all()
        paginator = Paginator(participant_list, 3)
        page = self.request.GET.get('page')
        context['pagination'] = paginator.get_page(page)
        return context


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


class KpiAssignUserView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiAssignForm
    success_message = 'Success: Kpi User was created.'
    success_url = reverse_lazy('kpiUserIndex')

    def form_valid(self, form):
        form = super(KpiAssignUserView, self).get_form()
        if self.request.POST.get('status') == 'Y':
            form.instance.is_suspended = True
            form.instance.individual_id = self.request.POST.get('individual')
            form.instance.status = 'Y'
        else:
            form.instance.is_suspended = False
            form.instance.individual_id = self.request.POST.get('individual')
            form.instance.status = 'N'
        return super(KpiAssignUserView, self).form_valid(form)


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


class KpiUserGroupUpdateView(BSModalUpdateView):
    model = KpiMembership
    template_name = 'kpis/update_kpi_group.html'
    form_class = KpiMembershipForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiUserIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership'] = KpiMembership.objects.filter(individual_id=int(self.kwargs['pk']))
        context['dropdown_dates'] = InputData.objects.all().values('value_date')
        return context


class KpiUserReadView(BSModalReadView):
    model = KpiIndividual
    template_name = 'kpis/read_kpi.html'


class KpiUserDeleteView(BSModalDeleteView):
    model = KpiIndividual
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi User was deleted.'
    success_url = reverse_lazy('kpiUserIndex')


class KpiGroupIndex(generic.ListView):
    model = KpiGroupset
    context_object_name = 'kpi_groups'
    template_name = 'kpis/group_index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dataset'] = KpiMembers.objects.all()
        return context


class KpiGroupCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = KpiGroupForm
    success_message = 'Success: Kpi Group was created.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiAssignGroupView(BSModalCreateView):
    template_name = 'kpis/create_kpi.html'
    form_class = GroupAssignedForm
    success_message = 'Success: Kpi Group was created.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiGroupUpdateView(BSModalUpdateView):
    model = KpiGroupset
    template_name = 'kpis/update_kpi.html'
    form_class = KpiGroupForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiMembershipView(BSModalCreateView):
    model = KpiMembers
    template_name = 'kpis/kpi_membership.html'
    form_class = KpiMembershipForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiGroupIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class KpiMembershipUpdateView(BSModalUpdateView):
    model = KpiMembers
    template_name = 'kpis/update_kpi.html'
    form_class = KpiMembershipForm
    success_message = 'Success: Kpi Group was updated.'
    success_url = reverse_lazy('kpiGroupIndex')


def remove_member(request, individual, group):
    member = KpiIndividual.objects.get(id=individual)
    group = KpiGroupset.objects.get(id=group)
    group.members.remove(member)
    return redirect('kpiGroupIndex')


class KpiGroupReadView(BSModalReadView):
    model = KpiGroupset
    template_name = 'kpis/read_kpi.html'


class KpiGroupDeleteView(BSModalDeleteView):
    model = KpiGroupset
    template_name = 'kpis/delete_kpi.html'
    success_message = 'Success: Kpi Group was deleted.'
    success_url = reverse_lazy('kpiGroupIndex')


class KpiValueIndex(generic.ListView):
    model = KpiValueset
    context_object_name = 'kpi_values'
    template_name = 'kpis/value_index.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kpi_values = KpiStats.objects.all()
        context['matching_string'] = str(self.request.POST.get('data', None))
        value_list = KpiStats.objects.all()
        paginator = Paginator(value_list, 4)
        page = self.request.GET.get('page')
        context['pagination'] = paginator.get_page(page)
        context['submit'] = self.request.GET.get('submit')
        context['date_data'] = get_value_dates(context['matching_string'])
        context['weight_data'] = get_weights(context['matching_string'])
        context['kpi_data_filters'] = ValueFilter(self.request.GET, queryset=kpi_values)
        context['data_values_filter'] = InputData.objects.all()
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        return context


class KpiValueCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi_individual_value.html'
    form_class = KpiValuesForm
    success_message = 'Success: Kpi Value was created.'
    success_url = reverse_lazy('kpiValueIndex')

    # def get(self, request, * args, ** kwargs):
    #     weights = self.request.GET.get('weight')
    #     return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        from datetime import date, datetime
        dateset = self.request.POST.get('values')
        if '.' in dateset:
            value_date = datetime.strptime(dateset.upper().replace("SEPT", "SEP"), "%b. %d, %Y")
        else:
            value_date = datetime.strptime(dateset, '%B %d, %Y')
        value = self.request.POST.get('value_set')
        kpis = self.request.POST.get('kpi')
        weights = get_weights(kpis).final_weight.item()
        # import pdb; pdb.set_trace()
        data = self.request.POST.get('content_set')
        individual = self.request.POST.get('individual')
        group = self.request.POST.get('group_set')
        contribution_to_performance = (float(weights) * float(value)) / 100
        KpiStats.objects.update_or_create(data_str=data, value_date=value_date, value=value, weights=weights, kpis=kpis,
                                          individual_id=individual, group=group,
                                          contribution_to_performance=contribution_to_performance)
        return redirect(reverse('kpiValueIndex'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        kpi_values = InputData.objects.all()
        inputs = InputData()
        inputs.value_date = self.request.POST.get('date_range')
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        kpi_values = InputData.objects.all()
        if self.request.method == 'GET':
            context['matching_string'] = str(self.request.GET.get('level', None))
            context['individual_checker'] = True
            context['submit'] = self.request.GET.get('submit')
            date_data = get_value_dates(context['matching_string'])
            context['date_data'] = date_data
            context['weight_data'] = get_weights(context['matching_string'])
            context['kpi_data_filters'] = ValueFilter(self.request.GET, queryset=kpi_values)
            current_number_of_levels = InputData.objects.aggregate(level_count=Count('number_of_levels', distinct=True))
            counts_ = current_number_of_levels['level_count']
            data_structures = []
            i = 0
            while i <= counts_:
                data_structures.append(
                    InputData.objects.filter(~Q(levelset_id=None) & Q(number_of_levels__exact=i) & Q(kpis=None)))
                i = i + 1
            context['data_values_filter'] = list(itertools.chain.from_iterable(data_structures))
            context['individuals_values_filter'] = KpiParticipants.objects.all()
            values_ = KpiValues.objects.all().only("value_date")
            context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        return context


class KpiGroupValueCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi_individual_value.html'
    form_class = KpiValueForm
    success_message = 'Success: Kpi Value was created.'
    success_url = reverse_lazy('kpiValueIndex')


    def post(self, request, *args, **kwargs):
        dateset = self.request.POST.get('values')
        if '.' in dateset:
            value_date = datetime.strptime(dateset.upper().replace("SEPT", "SEP"), "%b. %d, %Y")
        else:
            value_date = datetime.strptime(dateset, '%B %d, %Y')
        value = self.request.POST.get('value_set')
        kpis = self.request.POST.get('kpi')
        weights = get_weights(kpis).final_weight.item()
        individual = self.request.POST.get('individual')
        # import pdb; pdb.set_trace()
        group = self.request.POST.get('grouping')
        data = self.request.POST.get('content_set')
        contribution_to_performance = (float(weights) * float(value)) / 100
        KpiStats.objects.update_or_create(value_date=value_date, value=value, weights=weights, kpis=kpis, data_str=data,
                                          individual_id=individual, group=group,
                                          contribution_to_performance=contribution_to_performance)
        return redirect(reverse('kpiValueIndex'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        kpi_values = InputData.objects.all()
        context['matching_string'] = str(self.request.POST.get('data', None))
        context['group_checker'] = True
        context['submit'] = self.request.GET.get('submit')
        context['date_data'] = get_value_dates(context['matching_string'])
        context['weight_data'] = get_weights(context['matching_string'])
        context['kpi_data_filters'] = ValueFilter(self.request.GET, queryset=kpi_values)
        current_number_of_levels = InputData.objects.aggregate(level_count=Count('number_of_levels', distinct=True))
        counts_ = current_number_of_levels['level_count']
        data_structures = []
        i = 0
        while i <= counts_:
            data_structures.append(
                InputData.objects.filter(~Q(levelset_id=None) & Q(number_of_levels__exact=i) & Q(kpis=None)))
            i = i + 1
        context['data_values_filter'] = list(itertools.chain.from_iterable(data_structures))
        context['group_values_filter'] = KpiGroupset.objects.all()
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        return context


class KpiValueUpdateView(BSModalUpdateView):
    model = KpiValueset
    template_name = 'kpis/update_kpi.html'
    form_class = KpiValuesForm
    success_message = 'Success: Kpi Value was updated.'
    success_url = reverse_lazy('kpiValueIndex')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.request.POST.get('value_dates')
        data = KpiValueset()
        data.value = self.request.POST.get('value')
        data.value_date = self.request.POST.get('value_date')
        data.save()
        return redirect('kpiValueIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        return context


class KpiValueReadView(BSModalReadView):
    model = KpiValueset
    template_name = 'kpis/stats_summary.html'


def to_integer(dt_time):
    return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day


        

class KpiValueDeleteView(BSModalDeleteView):
    model = KpiValueset
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





def KpiStatsSummary(request):
    context = {}
    if request.method == "GET":
            date_required = request.GET.get('start_date',None)
            # import pdb; pdb.set_trace()
            end_date = request.GET.get('end_date',None)
            kpiindividual = request.GET.get('kpi_set')
            # get_data = KpiStats.objects.get(pk=pk)
            # get_individual = KpiParticipants.objects(pk=get_data.individual_id)
            context['kpi_users'] = KpiParticipants.objects.all()
            if date_required:
                cleaned_date = datetime.strptime(date_required, '%Y-%m-%d')
                ended_date = datetime.strptime(end_date, '%Y-%m-%d')
                lastday = []
                # import pdb; pdb.set_trace()
                for month in range(cleaned_date.month, ended_date.month+1):
                        # import datetime
                        # import pdb;pdb.set_trace()
                        currentdate = lastdayofmonth(date(2020, month, 1))
                        # import pdb;pdb.set_trace()
                        summation = KpiStats.objects.filter(Q(value_date=currentdate) & Q(individual_id__individual=kpiindividual)) \
                        .aggregate(sum=Sum('contribution_to_performance'))
                        summation.update({'vdate':currentdate})
                        lastday.append(summation)
                context['summation'] = lastday
                # import pdb;pdb.set_trace()
                # context['member_average'] = KpiStats.objects.filter(Q(value_date=cleaned_date) & Q(individual_id=get_data.individual_id)).aggregate(
                # avg=Avg('value'))
    return render(request,'kpis/stats_summary.html',context)

def print_view(request):
    html = HTML('kpis/stats_summary.html')
    html.write_pdf(target='tmp/stats.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('stats.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response

def sending_results(request):
    subject = request.POST.get('subject', '')
    # print(subject)
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if request.method == 'POST':
        send_mail(subject, message, from_email, ['tutorialcreation81@gmail.com', 'martin.bironga@actserv.co.ke'])
        return render(request, 'kpis/stats_summary.html')
    return redirect('kpiValueIndex')


############################
## get a kpis details #####
###########################

def specific_kpi(request):
    context = {}  # takes the context argument
    template_name = 'kpis/dropdown_lists.html'  # our redirect page
    kpis = request.GET.get('kpi_val')
    collected_kpi = request.GET.get('kpi_date')
    weight = str(request.GET.get('weight', None))
    context['kpi_data'] = get_kpis(kpis)
    context['date_data'] = get_value_dates(collected_kpi)
    # context['weight_data'] = get_weights(weight)
    return render(request, template_name, context)
