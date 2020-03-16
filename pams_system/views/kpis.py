from datetime import date, datetime
import pandas as pd
import itertools
from django.db.models import F
from django.db.models import Q, Sum, Avg, Count, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
# from django_pandas.io import read_frame
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
from pams_system.utils.search_algorithms import get_value_dates, get_weights, get_kpis
from pams_system.filters import ValueFilter


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
        # Add in the publisher
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
        # Call the base implementation first to get a context
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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # context['membership'] = KpiMembers.objects.filter(group_id=int(self.kwargs['pk']))
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
        # print(self.request.GET.get('level'))
        context['matching_string'] = str(self.request.POST.get('data', None))
        # import pdb;pdb.set_trace()
        # print(context['matching_string'])
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

    def post(self, request, *args, **kwargs):
        # stats = KpiStats()
        from datetime import date, datetime
        # dates = date(self.request.POST.get('values'))
        # print(dates)
        # import pdb;  pdb.set_trace()
        dateset = self.request.POST.get('values')
        if '.' in dateset:
            value_date = datetime.strptime(dateset, '%b. %d, %Y')
        else:
            value_date = datetime.strptime(dateset, '%B %d, %Y')
        value = self.request.POST.get('value_set')
        weights = self.request.POST.get('weight')
        kpis = self.request.POST.get('kpi')
        data = self.request.POST.get('content_set')
        individual = self.request.POST.get('ind')
        group = self.request.POST.get('group_set')
        contribution_to_performance = (float(weights) * float(value)) / 100
        # stats.save()
        KpiStats.objects.update_or_create(data_str=data, value_date=value_date, value=value, weights=weights, kpis=kpis,
                                          individual=individual, group=group,
                                          contribution_to_performance=contribution_to_performance)
        print(contribution_to_performance)
        # print(self.request.POST)
        # print(self.request.GET.get('level'))
        # form = self.form_class()
        # print(form)
        return redirect(reverse('kpiValueIndex'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        values_ = KpiValues.objects.all().only("value_date")
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        # query = str(InputData.objects.all().query)
        # df = pd.read_sql_query(query, connection)
        kpi_values = InputData.objects.all()
        inputs = InputData()
        inputs.value_date = self.request.POST.get('date_range')
        context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
        # query = str(InputData.objects.all().query)
        # df = pd.read_sql_query(query, connection)
        kpi_values = InputData.objects.all()
        # if self.request.is_ajax:
        # print(self.request.is_ajax)
        # matching_string = self.request.GET.get('level')
        # print(self.request.GET.get('level'))
        # print()
        if self.request.method == 'GET':
            context['matching_string'] = str(self.request.GET.get('level', None))
            # print(context['matching_string'])
            # import pdb;pdb.set_trace()
            # print(context['matching_string'])
            context['individual_checker'] = True
            context['submit'] = self.request.GET.get('submit')
            date_data = get_value_dates(context['matching_string'])
            # print(date_data)
            context['date_data'] = date_data
            # print(context['date_data'])
            context['weight_data'] = get_weights(context['matching_string'])
            context['kpi_data_filters'] = ValueFilter(self.request.GET, queryset=kpi_values)
            current_number_of_levels = InputData.objects.aggregate(level_count=Count('number_of_levels', distinct=True))
            counts_ = current_number_of_levels['level_count']
            data_structures = []
            # print(request.is_ajax)
            i = 0
            while i <= counts_:
                data_structures.append(
                    InputData.objects.filter(~Q(levelset_id=None) & Q(number_of_levels__exact=i) & Q(kpis=None)))
                i = i + 1
            # import pdb; pdb.set_trace()
            # for i in data_structures:
            context['data_values_filter'] = list(itertools.chain.from_iterable(data_structures))
            # context['data_values_filter'] = InputData.objects.all()
            context['individuals_values_filter'] = KpiParticipants.objects.all()
            values_ = KpiValues.objects.all().only("value_date")
            context['date_values'] = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]
            # return render(self.request,'kpis/dropdown_lists.html')
        # if self.request.method == "POST":
        # stats = KpiStats()
        # stats.value_date = self.request.POST.get('values')
        # stats.value = self.request.POST.get('value_set')
        # stats.weights = self.request.POST.get('weight')
        # stats.kpis = self.request.POST.get('content_set')
        # stats.individual = self.request.POST.get('ind')
        # stats.group = self.request.POST.get('group_set')
        # stats.contribution_to_performance = float(stats.weights) * float(stats.value)
        # # stats.save()
        # print(stats.contribution_to_performance)
        # return render(self.request,'kpis/value_index.html',context)
        # stats.save()
        # import pdb; pdb.set_trace()
        # print(self.request.POST.get('values'))
        # print(self.request.POST.get('value_set'))
        # print(self.request.POST.get('weight'))
        # print(self.request.POST.get('content_set'))
        # print(self.request.POST.get('ind'))
        # print(self.request.POST.get('group_set'))
        # if self.request.method=='POST':
        #     print('\n\n\n\n',self.request.POST, '\n\n\n\n\n import pdb; pdb.set_trace()')
        return context


class KpiGroupValueCreateView(BSModalCreateView):
    template_name = 'kpis/create_kpi_individual_value.html'
    form_class = KpiValueForm
    success_message = 'Success: Kpi Value was created.'
    success_url = reverse_lazy('kpiValueIndex')

    # values_ = KpiValues.objects.all().only("value_date")

    # date_values = [v.value_date.value_date.strftime("%Y-%m-%d") for v in values_ if v.value_date]

    def post(self, request, *args, **kwargs):
        # stats = KpiStats()
        # dates = date(self.request.POST.get('values'))
        # print(dates)
        # import pdb;  pdb.set_trace()
        # dateset = self.request.POST.get('values')
        # datetime.strptime(dateset, '%b. %d, %Y')
        dateset = self.request.POST.get('values')
        if '.' in dateset:
            value_date = datetime.strptime(dateset, '%b. %d, %Y')
        else:
            value_date = datetime.strptime(dateset, '%B %d, %Y')
        value = self.request.POST.get('value_set')
        weights = self.request.POST.get('weight')
        kpis = self.request.POST.get('kpi')
        individual = self.request.POST.get('ind')
        group = self.request.POST.get('grouping')
        data = self.request.POST.get('content_set')
        contribution_to_performance = (float(weights) * float(value)) / 100
        # stats.save()
        KpiStats.objects.update_or_create(value_date=value_date, value=value, weights=weights, kpis=kpis, data_str=data,
                                          individual=individual, group=group,
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
        # print(request.is_ajax)
        i = 0
        while i <= counts_:
            data_structures.append(
                InputData.objects.filter(~Q(levelset_id=None) & Q(number_of_levels__exact=i) & Q(kpis=None)))
            i = i + 1
        # import pdb; pdb.set_trace()
        # for i in data_structures:
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


class KpiStatsSummary(BSModalReadView):
    model = KpiStats
    template_name = 'kpis/stats_summary.html'

    def get(self, request, *args, **kwargs):
        context = {}
        # print(22)
        if self.request.GET.get('value_date'):
            date_required = self.request.GET.get('value_date')
            cleaned_date = datetime.strptime(date_required, '%Y-%m-%d')
        # date_required = datetime(self.request.GET.get('value_date'))
        # print(date_required)
        # import pdb; pdb.set_trace()
            context['member_average'] = KpiStats.objects.filter(value_date=cleaned_date).aggregate(
                avg=Avg('value'))
        return render(request,'kpis/stats_summary.html',context)
        # return super(KpiStatsSummary, self).get(request, context)

    def get_context_data(self, **kwargs):
        from datetime import date
        context = super().get_context_data(**kwargs)
        # print(self.kwargs['pk'])
        # import pdb;pdb.set_trace()
        context['key'] = int(self.kwargs['pk'])
        context['data'] = KpiStats.objects.filter(pk=self.kwargs['pk'])
        context['member_sum'] = KpiStats.objects.filter(pk=self.kwargs['pk']).aggregate(Sum('value'))
        # import pdb; pdb.set_trace()
            # return render(self.request,'kpis/stats_summary.html',context)
        # return redirect(reverse_lazy('kpiValueIndex'))

        # context['member_ranking'] = KpiValueset.objects.filter(Q(tree_id=self.kwargs['tree_id'])).annotate(
        #     Max('value')).order_by('-value__max')
        # context['group_sum'] = KpiValueset.objects.filter(
        #     Q(kpi_level__gte=0) & Q(tree_id=self.kwargs['tree_id'])).aggregate(Sum('value'))
        # context['group_average'] = KpiValueset.objects.filter(
        #     Q(kpi_level__gte=0) & Q(tree_id=self.kwargs['tree_id'])).aggregate(Avg('value'))
        # import pdb; pdb.set_trace()
        # dataset_one = KpiValueset.objects.filter(Q(kpi_level__gte=0)).aggregate(Sum('value'))
        # dataset_two = KpiValueset.objects.filter(Q(tree_id=self.kwargs['tree_id'])).aggregate(Sum('value'))
        # group_rankings = {k: dataset_two[k] / dataset_one[k] * 100 for k in dataset_one.keys() & dataset_two}
        # context['group_ranking'] = {k: dataset_two[k] / dataset_one[k] * 100 for k in dataset_one.keys() & dataset_two}
        # ranks = self.model()
        # ranks.rank = group_rankings['value__sum']
        # import  pdb; pdb.set_trace()
        # ranks.save()
        return context


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


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def print_view(request):
    buffer = io.BytesIO()
    # creating the pdf object
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello world!..")
    # close pdf object
    p.showPage()
    p.save()
    # fileresponse sets content disposition header so that
    # browser presents option to save the file
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="first pdf file generated")


from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def sending_results(request):
    subject = request.POST.get('subject', '')
    print(subject)
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
    context['weight_data'] = get_weights(weight)
    return render(request, template_name, context)
