import datetime
import itertools
from django.db.models import Q, F, Sum, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.forms import modelformset_factory
from dateutil.parser import parse
# from django_pandas.io import read_frame
from django.utils import timezone
from pams_system.filters import WeightFilter
from pams_system.utils.search_algorithms import get_kpis

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from pams_system.forms.levelforms import (LevelStructureForm, LevelListForm, LevelTypeForm, KPIWeightForm,
                                          KpiStructureForm,
                                          )
from pams_system.models.maps import MapType, MapList
from pams_system.models.levels import InputData, Level, KPIWeight, KPIWeightings

#########################
### class-based views ###
#########################

from setup import celery_app


@celery_app.task(name="test-celery-2")
def test_celery():
    print("test working >>>>>>>>>>>>>")


# in the class below we will initialize the form
# using this class based view
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    # Execute every three hours.
    'add-after-two-minutes': {
        'task': 'test-celery-2',
        'schedule': crontab(minute=0, hour=0),
    },
}


# This class based view is aimed at filtering the data
# based on the id and therefore we shall use the data from previous class
class LevelStructureIndex(generic.ListView):
    model = InputData
    template_name = 'levels/datastructures.html'
    test_celery.delay()

    # bread_crumbs = InputData.get_levels.all()

    def get_queryset(self):
        self.maplist = InputData.objects.filter(
            # we will filter the maplist and level
            Q(maplist_id__maplist_name=self.kwargs['maplist'])  # for distinctly identifying the maplis
        )
        return InputData.objects.filter(
            Q(maplist_id__maplist_name=self.maplist)  # filters for the maplist
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        # context['breadcrumbs'] = self.bread_crumbs.all()[:1]
        context['levels'] = self.maplist
        # print(len(self.maplist))
        context['choices'] = InputData.objects.all()
        return context


class DataStructure(generic.ListView):
    model = InputData
    context_object_name = 'levels'
    template_name = 'levels/datastructure.html'

    def get_queryset(self):
        self.maplist = InputData.objects.filter(
            # we will filter the maplist and level
            Q(maplist_id=int(self.kwargs['maplist_pk'])) &  # for distinctly identifying the maplis
            Q(name=self.kwargs['strategic_objective']) &  # for distinctly identifying the strategic objective
            Q(tree_id=int(self.kwargs['tree_pk']))  # for distinctly identifying which tree it belongs to
        )
        self.tree_pk = self.kwargs['tree_pk']  # obtaining the tree_id in order to use it on filtering.

        return InputData.objects.filter(
            Q(maplist_id=int(self.maplist[0].maplist_id)) &  # filters for the maplist
            Q(name=self.maplist[0].name) &  # filters for the strategic objective
            Q(tree_id=int(self.maplist[0].tree_id))  # filters for the specific tree
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['levels'] = self.maplist
        context['levelset'] = self.model.objects.filter(
            tree_id__exact=int(self.tree_pk))  # for querying the distinct tree
        context['dataset'] = self.model.objects.all()
        return context


class LevelStructureCreateView(BSModalCreateView, generic.FormView):
    template_name = 'levels/create_datastructures.html'
    # template_name = 'levels/read_level.html'
    form_class = LevelStructureForm
    success_message = 'Success: Data was created.'
    # success_url = reverse_lazy('levelStructureIndex')

    # def get_object(self,request, *args,**kwargs):
    #     parent = request.GET.get('parent')
    #     return parent
    # def get_previous(request,parent):
    # context = {}
    # data = get_kpis(request.GET.get('data_str'))
    # return render(request, 'levels/kpi_dropdown_list.html', context)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Attach Data Structure'
        context['check_data_str'] = True
        # import pdb; pdb.set_trace()
        # print(self.request.is_ajax)

        parent_id = self.request.GET.get('parent')
        # parent=get_object()
        # print(parent_id)
        if parent_id:
            child = InputData.objects.get(pk=parent_id)
            context['levelset'] = Level.objects.filter(
                Q(maplist_id=child.maplist_id) & Q(maptype_id=child.maptype_id))
            context['parentset'] = child.get_next_sibling()
            return render(self.request, self.template_name, context)
            # import pdb;pdb.set_trace()
        return context



    def form_valid(self, form):
        data = form.cleaned_data
        # datass =self.request.GET.get('parent')
        data['maptype_id']=self.request.GET.get('maptype_id', '')
        # import pdb;pdb.set_trace()
        data['maplist_id']=self.request.GET.get('maplist_id', '')
        get_level = Level.objects.get(name=self.request.POST.get('datastructure'))
        data['levelset_id'] = get_level.main_id
        data['is_datastructure']=True
        # import pdb;pdb.set_trace()
        data['previous_datastructure'] = self.request.POST.get('datastructure')
        # print(form)
        # import pdb;pdb.set_trace()
        # print(self.request.is_ajax)
        # import pdb;pdb.set_trace()
        input_data = InputData.objects.update_or_create(**data)
        return redirect(reverse("levelStructureIndex", kwargs={
            'maplist': input_data[0].maplist
        }))
        # return redirect(reverse("dataStructureIndex", kwargs={
        #     'maplist_pk': input_data[0].maplist,
        #     'strategic_objective': input_data[0].name,
        #     'tree_pk': input_data[0].tree_id,
        # }))

    

class KpiStructureCreateView(BSModalCreateView, generic.FormView):
    template_name = 'levels/create_kpitypes.html'
    form_class = KpiStructureForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('levelStructureIndex')


    def post(self, request, *args, **kwargs):
        maptype = self.request.GET.get('maptype_id')
        maplist = self.request.GET.get('maplist_id')
        # levelset = self.request.POST.get('levelset')
        parent = self.request.POST.get('parent')
        get_level = InputData.objects.get(pk=parent)
        levelset = get_level.levelset_id
        # import pdb; pdb.set_trace()
        kpis = self.request.POST.get('kpis')
        previous_datastructure = self.request.POST.get('kpi_node')
        value_date = self.request.POST.get('process_date')
        parsed_dates = [parse(d).date() for d in value_date.split(",")]
        # import pdb;pdb.set_trace()
        InputData.objects.create(name=kpis,maptype_id=maptype, maplist_id=maplist, levelset_id=levelset,
                                           parent_id=parent, kpis=kpis, value_date=parsed_dates,
                                           previous_datastructure=previous_datastructure, is_kpi=True)
        # import pdb;pdb.set_trace()
        data_check = MapList.objects.get(maplist_id=int(self.request.GET.get('maplist_id')))
        return redirect(reverse("levelStructureIndex", kwargs={
            'maplist': data_check.maplist_name
        }))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kpi_str'] = 'Create'
        # level_up = InputData.objects.filter(pk=int(self.kwargs['pk'])) 
        # import pdb; pdb.set_trace()
        # child = InputData.objects.get(pk=self.kwargs['pk'])
        # context['levelset'] = Level.objects.filter(
        #     Q(maplist_id=child.maplist_id) & Q(maptype_id=child.maptype_id))
        # import pdb; pdb.set_trace()
        # context['parentsets'] = level_up | level_up.get_ancestors()
        context['dates'] = self.request.GET.get('dates')
        return context



class LevelStructureUpdateView(BSModalUpdateView, generic.FormView):
    model = InputData
    template_name = 'levels/update_level.html'
    form_class = LevelStructureForm
    success_message = 'Success: Data was updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("dataStructureIndex", kwargs={
            'maplist_pk': form.instance.maplist_id,
            'strategic_objective': form.instance.name,
            'tree_pk': form.instance.tree_id,
        }))


class LevelStructureReadView(BSModalUpdateView, generic.FormView):
    model = InputData
    template_name = 'levels/read_level.html'
    # context_object_name = 'levels'
    form_class = LevelTypeForm
    success_message = 'Success: Data was updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = InputData.objects.all()
        return context

    def form_valid(self, form):
        weights = self.request.POST('kpi_weights')
        # print(weights)
        form.save()
        return redirect(reverse("dataStructureIndex", kwargs={
            'maplist_pk': form.instance.maplist_id,
            'strategic_objective': form.instance.name,
            'tree_pk': form.instance.tree_id,
        }))


class LevelStructureDeleteView(BSModalDeleteView, generic.FormView):
    model = InputData
    template_name = 'levels/delete_level.html'
    success_message = 'Success: Data was successfully deleted.'

    # success_url = reverse_lazy('dataStructureIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("dataStructureIndex", kwargs={
            'maplist_pk': form.instance.maplist_id,
            'strategic_objective': form.instance.name,
            'tree_pk': form.instance.tree_id,
        }))


class LevelReadView(BSModalReadView, generic.FormView):
    model = Level
    template_name = 'level/read_level.html'

    # from setup import  celery_app
    # @celery_app.task(name="test-celery-2")
    # def test_celery(self):
    #     print("test working >>>>>>>>>>>>>")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("levelIndex", kwargs={
            'maplist': form.instance.maplist
        }))


class LevelIndex(generic.ListView):
    model = Level
    context_object_name = 'levels'
    template_name = 'levels/index.html'
    success_url = reverse_lazy('levelIndex')

    def get_queryset(self):
        self.maplist = Level.objects.filter(maplist_id__maplist_name=self.kwargs['maplist'])
        return Level.objects.filter(maplist_id__maplist_name=self.maplist)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['levels'] = self.maplist
        return context


class LevelUpdateView(BSModalUpdateView, generic.FormView):
    model = Level
    template_name = 'levels/update_level.html'
    form_class = LevelListForm
    success_message = 'Success: Level was updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("levelIndex", kwargs={
            'maplist': form.instance.maplist
        }))


#

class LevelListCreateView(BSModalCreateView):
    template_name = 'levels/create_level.html'
    form_class = LevelListForm
    success_message = 'Success: Level was created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        context['parentset'] = InputData.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        data['maptype_id']=self.request.GET.get('maptype_id', '')
        data['maplist_id']=self.request.GET.get('maplist_id', '')
        level = Level.objects.update_or_create(**data)
        return redirect(reverse("levelIndex", kwargs={
            'maplist': level[0].maplist
        }))


class LevelDeleteView(BSModalDeleteView):
    model = Level
    template_name = 'levels/delete_level.html'
    success_message = 'Success: Level was deleted.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("levelIndex", kwargs={
            'maplist': form.instance.maplist
        }))


############################
## function-based views ####
############################

#######################################
# handling dependent-chained dropdown #
#######################################
def specific_maplist(request):
    context = {}  # takes the context argument
    template_name = 'levels/dropdown_lists.html'  # our redirect page
    maptype_id = request.GET.get('maptype_data')
    maplist_id = request.GET.get('maplist_data')
    levelset_id = request.GET.get('level_data')
    # collect the maplist_id
    context['maptypes'] = MapList.objects.filter(
        Q(maptype_name_id=maptype_id))  # match the collected maplist_id and maplist
    context['levelset'] = Level.objects.filter(Q(maplist_id=maplist_id)) 
     # match the collected maplist_id and maplist
    # if levelset_id and not maplist_id:
    #     context['data_str'] = InputData.objects.filter(
    #         Q(levelset_id=int(levelset_id)))  # match the collected maplist_id and maplist
    # then present the data for that specific maplist
    # import pdb; pdb.set_trace()
    return render(request, template_name, context)


#######################################
# handling dependent-chained dropdown #
# for the specific previous_level     #
#######################################
def specific_previous_level(request):
    context = {}  # takes the context argument
    template_name = 'levels/dropdown_lists.html'  # our redirect page
    maplist_id = request.GET.get('maplist_data')  # collect the maplist_id
    context['levelset'] = Level.objects.filter(maplist_id=maplist_id)  # match the collected maplist_id and maplist
    # then present the data for that specific maplist
    return render(request, template_name, context)


####################################
## function for adding weights ###
##################################

def castToList(x):  # casts x to a list
    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        return [x]
    try:
        return list(x)
    except TypeError:
        return [x]


def add_weights(request):
    context = {}
    template_name = 'levels/add_weights.html'
    context['levels'] = InputData.objects.all()
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
    context['data_str'] = list(itertools.chain.from_iterable(data_structures))
    # import pdb; pdb.set_trace()
    # if request.method == 'GET':
    #     kpi_data = get_kpis(request.GET.get('data_str_id'))
    #     return render(request,'levels/kpi_dropdown_list.html',{'kpi_data':kpi_data})
    # redirect('add_kpi_weights')

    context['kpi_data'] = InputData.objects.all()
    kpi_set = request.POST.get('kpi_set')
    # if request.is_ajax:
        # context['kpi_data'] = InputData.objects.filter(name=request.GET.get('data_str'))
    form = KPIWeightForm(request.POST or None)
    context['form'] = form
    # the computation algorithm for weight allocation in the specific levels
    # if form.is_valid():
    # form.save()
    # for index in range(0, 1):
    ''' 
    Ensure index can be picked dynamically.
    '''
    if request.method == 'POST':
        index = InputData.objects.filter(name=request.POST.get('kpi_set')).first().number_of_levels
        level = InputData.objects.filter(name=request.POST.get('kpi_set')).first().levelset_id
        kpi_pk = InputData.objects.filter(name=request.POST.get('kpi_set')).first().pk
        pk = InputData.objects.filter(name=request.POST.get('data_str')).first().pk
        effective_date = parse(request.POST.get('effective_date')).date()
        weight = request.POST.get('weight')
        kpis = request.POST.get('kpi_set')
        KPIWeightings.objects.update_or_create(content_id=kpi_pk, kpis=kpis,
                                               effective_date=effective_date,
                                               weight=weight)
        # print(index)
        # import pdb;
        # pdb.set_trace()

        valid_data = KPIWeightings.objects.filter(
            Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                content_id__parent_id=pk))
        if pk:
            if request.POST.get('weight') == None:
                each_weight = 0
            else:
                each_weight = request.POST.get('weight')
            context['total_weight_0'] = KPIWeightings.objects.filter(
                Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                    content_id__parent_id=pk)
            ).aggregate(
                Sum('weight'))
            context['data'] = KPIWeightings.objects.filter(
                Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                    content_id__parent_id=pk)
            ).values(
                "content_id__name").annotate(
                Count("content_id"),
                val=F('weight'), sum=Sum('weight'),
                content=F('content'),
                final_weight=F(
                    'final_weight')).last()
            dataset =  InputData.objects.filter(
                Q(levelset_id=level) & Q(number_of_levels__exact=index) & Q(
                    parent_id=pk)).values(
                "name").annotate(Count("pk"))
            weight_set = []
            for indexes in range(0, len(dataset)):
                weight_set.insert(indexes, KPIWeightings.objects.filter(
                    content_id__name=dataset[indexes]['content_id__name']).values('weight').annotate(
                    content=F('content_id__name')).order_by('-created_at').first())
            context['weightings'] = weight_set
            # import pdb; pdb.set_trace()
            # performing the computations
            import pandas as pd
            values = pd.DataFrame(weight_set)
            weights = values.weight
            total_weight = weights.sum(axis=0)
            context['totals'] = total_weight
            percentage = (weights / total_weight) * 100
            percentages = list(percentage)
            data = zip(percentages, weight_set)
            context['datasets'] = list(data)
            # context['datasets'] = KPIWeightings.objects.filter(
            #         content_id__name=dataset[0]['content_id__name']).order_by('-created_at').first()
            # if request.method == 'POST':
            # form = KPIWeightForm(request.POST or None
            # import pdb; pdb.set_trace()
            keyset = []
            for key, val in values.content.items():
                if val == str(request.POST.get('kpi_set')):
                    keyset.append(int(key))

            context['calculated_weight'] = (int(each_weight) / context['total_weight_0'][
                'weight__sum']) * 100
            KPIWeightings.objects.update_or_create(content_id=kpi_pk, kpis=kpis,
                                                   effective_date=effective_date,
                                                   weight=weight, final_weight=percentages[keyset[0]])
        # weight filters
        # import pdb; pdb.set_trace()
        # form.save()

        # environment_variables
        # context['strategic_objectives'] = int(request.POST.get('content'))
        # print(context['strategic_objectives'])
    '''
    Ensure the weight_listing is sorted dynamically
    '''
    current_number_of_levels = InputData.objects.aggregate(level_count=Count('number_of_levels', distinct=True))
    counts_ = current_number_of_levels['level_count']
    range(0, counts_)

    # import  pdb; pdb.set_trace()
    # print('\n\n\n\n\n\n', request.POST, '\n\n\n\n\n\n\n\n\n')
    # if request.is_ajax:
    #     data = request.GET.get('content_id')
    #     get = InputData.objects.filter(pk=data).first().number_of_levels
    #     print(get)
    #     if request.method == "POST":
    #     pk = InputData.objects.filter(name=request.POST.get('kpi_set')).first().number_of_levels
    #     context['form'] = form
    #     if pk == 0:
    #         weight_list = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list)
    #         context['filter'] = weight_filter
    #     if pk == 1:
    #         weight_list_1 = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list_1)
    #         context['filter_1'] = weight_filter
    #     if pk == 2:
    #         weight_list_2 = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list_2)
    #         context['filter_2'] = weight_filter
    return render(request, template_name, context)


#


def get_kpisets(request):
    context = {}
    if request.method == 'GET':
        context['kpi_data'] = get_kpis(request.GET.get('data_str'))
    return render(request, 'levels/kpi_dropdown_list.html', context)

def get_previous(request,parent):
    context = {}
    if request.method == 'GET':
        context['kpi_data'] = get_kpis(request.GET.get('data_str'))
    return render(request, 'levels/kpi_dropdown_list.html', context)



#

def populate_forms(request,pk):
    context = {}
    template_name = 'levels/add_weights.html'
    context['levels'] = InputData.objects.all()
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
    context['data_str'] = list(itertools.chain.from_iterable(data_structures))
    # import pdb; pdb.set_trace()
    # if request.method == 'GET':
    #     kpi_data = get_kpis(request.GET.get('data_str_id'))
    #     return render(request,'levels/kpi_dropdown_list.html',{'kpi_data':kpi_data})
    # redirect('add_kpi_weights')

    context['kpi_data'] = InputData.objects.filter(~Q(levelset_id=None) & Q(parent_id=pk))
    kpi_set = request.POST.get('kpi_set')
    # if request.is_ajax:
        # context['kpi_data'] = InputData.objects.filter(name=request.GET.get('data_str'))
    form = KPIWeightForm(request.POST or None)
    context['form'] = form
    # the computation algorithm for weight allocation in the specific levels
    # if form.is_valid():
    # form.save()
    # for index in range(0, 1):
    ''' 
    Ensure index can be picked dynamically.
    '''
    # form processing
    # print(request.POST)
    if request.method == 'POST':
        # import  pdb; pdb.set_trace()
        # print(request.POST)
        # if form.is_valid():
        # if request.POST.get('kpi_set') and request.POST.get('data_str'):
        index = InputData.objects.filter(name=request.POST.get('kpi_set')).first().number_of_levels
        level = InputData.objects.filter(name=request.POST.get('kpi_set')).first().levelset_id
        kpi_pk = InputData.objects.filter(name=request.POST.get('kpi_set')).first().pk
        # primary_key = InputData.objects.filter(name=request.POST.get('data_str')).first().pk
        effective_date = parse(request.POST.get('effective_date')).date()
        weight = request.POST.get('weight')
        kpis = request.POST.get('kpi_set')
        KPIWeightings.objects.create(content_id=kpi_pk, kpis=kpis,
                                               effective_date=effective_date,
                                               weight=weight)
        # print(index)
        # import pdb;
        # pdb.set_trace()

        valid_data = KPIWeightings.objects.filter(
            Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                content_id__parent_id=pk))
        if pk:
            if request.POST.get('weight') == None:
                each_weight = 0
            else:
                each_weight = request.POST.get('weight')
            context['total_weight_0'] = KPIWeightings.objects.filter(
                Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                    content_id__parent_id=pk)
            ).aggregate(
                Sum('weight'))
            context['data'] = KPIWeightings.objects.filter(
                Q(content_id__levelset_id=level) & Q(content_id__number_of_levels__exact=index) & Q(
                    content_id__parent_id=pk)
            ).values(
                "content_id__name").annotate(
                Count("content_id"),
                val=F('weight'), sum=Sum('weight'),
                content=F('content'),
                final_weight=F(
                    'final_weight')).last()
            dataset = InputData.objects.filter(
                Q(levelset_id=level) & Q(number_of_levels__exact=index) & Q(
                    parent_id=pk)).values(
                "name").annotate(Count("pk"))
            weight_set = []
            for indexes in range(0, len(dataset)):
                weight_set.insert(indexes, KPIWeightings.objects.filter(
                    content_id__name=dataset[indexes]['name']).values('weight').annotate(
                    content=F('content_id__name')).order_by('-created_at').first())
            context['weightings'] = weight_set
            # import pdb; pdb.set_trace()
            # performing the computations
            import pandas as pd
            values = pd.DataFrame(weight_set)
            weights = values.weight
            total_weight = weights.sum(axis=0)
            context['totals'] = total_weight
            percentage = (weights / total_weight) * 100
            percentages = list(percentage)
            data = zip(percentages, weight_set)
            context['datasets'] = list(data)
            # context['datasets'] = KPIWeightings.objects.filter(
            #         content_id__name=dataset[0]['content_id__name']).order_by('-created_at').first()
            # if request.method == 'POST':
            # form = KPIWeightForm(request.POST or None
            # import pdb; pdb.set_trace()
            keyset = []
            for key, val in values.content.items():
                if val == str(request.POST.get('kpi_set')):
                    keyset.append(int(key))

            # context['calculated_weight'] = (int(each_weight) / context['total_weight_0'][
            #     'weight__sum']) * 100
            # if dataset:
            # import pdb;pdb.set_trace()
            KPIWeightings.objects.create(content_id=kpi_pk, kpis=kpis,
                                                   effective_date=effective_date,
                                                   weight=weight, final_weight=percentages[keyset[0]])
        # weight filters
        # import pdb; pdb.set_trace()
        # form.save()

        # environment_variables
        # context['strategic_objectives'] = int(request.POST.get('content'))
        # print(context['strategic_objectives'])
    '''
    Ensure the weight_listing is sorted dynamically
    '''
    current_number_of_levels = InputData.objects.aggregate(level_count=Count('number_of_levels', distinct=True))
    counts_ = current_number_of_levels['level_count']
    range(0, counts_)

    weight_list = KPIWeightings.objects.all()
    # weight_lists = KPIWeightings.objects.filter(pk=pk)
    context['weight_filter'] = WeightFilter(request.GET,queryset=weight_list) 
    # print(context['weight_filter'].form)

    # import  pdb; pdb.set_trace()
    # print('\n\n\n\n\n\n', request.POST, '\n\n\n\n\n\n\n\n\n')
    # if request.is_ajax:
    #     data = request.GET.get('content_id')
    #     get = InputData.objects.filter(pk=data).first().number_of_levels
    #     print(get)
    #     if request.method == "POST":
    #     pk = InputData.objects.filter(name=request.POST.get('kpi_set')).first().number_of_levels
    #     context['form'] = form
    #     if pk == 0:
    #         weight_list = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list)
    #         context['filter'] = weight_filter
    #     if pk == 1:
    #         weight_list_1 = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list_1)
    #         context['filter_1'] = weight_filter
    #     if pk == 2:
    #         weight_list_2 = KPIWeightings.objects.filter(
    #             ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
    #         weight_filter = WeightFilter(request.GET, queryset=weight_list_2)
    #         context['filter_2'] = weight_filter
    return render(request, template_name, context)


def get_previous_data_str(request):
    context={}
    parents = request.GET.get('parent')
    child = InputData.objects.filter(pk=int(parents))
    # import pdb;pdb.set_trace()
    if child:
        get_parent_level= Level.objects.filter(name=child[0].levelset)
        parent_pk=get_parent_level[0].pk
        context['parentset']=Level.objects.filter(previous_level_id=parent_pk)

    return render(request,'levels/dropdowns.html',context)


# def get_previous_data_kpi(request):
#     context={}
#     parent_id=request.GET.get('kpi_parent')
#     level_up = InputData.objects.filter(pk=parent_id)

#     # import pdb; pdb.set_trace()
#     child = InputData.objects.get(pk=parent_id)
#     # context['levelset'] = Level.objects.filter(
#     #     Q(maplist_id=child.maplist_id) & Q(maptype_id=child.maptype_id))
#     # import pdb; pdb.set_trace()
#     if child:
#         get_parent_level= Level.objects.filter(name=child[0].levelset)
#         parent_pk=get_parent_level[0].pk
#         context['parentsets']=Level.objects.filter(previous_level_id=parent_pk)

#     return render(request,'levels/dropdowns.html',context)