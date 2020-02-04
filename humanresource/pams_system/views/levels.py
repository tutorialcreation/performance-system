import datetime
from django.db.models import Q, F, Sum, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.forms import modelformset_factory
# from django_pandas.io import read_frame
from django.utils import timezone
from pams_system.filters import WeightFilter

from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView)

from pams_system.forms.levelforms import LevelStructureForm, LevelListForm, LevelTypeForm, KPIWeightForm
from pams_system.models.maps import MapType, MapList
from pams_system.models.levels import InputData, Level, KPIWeight, KPIWeightings


#########################
### class-based views ###
#########################


# in the class below we will initialize the form
# using this class based view

# This class based view is aimed at filtering the data
# based on the id and therefore we shall use the data from previous class
class LevelStructureIndex(generic.ListView):
    model = InputData
    template_name = 'levels/datastructures.html'

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

        # return InputData.objects.all()
        return InputData.objects.filter(
            Q(maplist_id=int(self.maplist[0].maplist_id)) &  # filters for the maplist
            Q(name=self.maplist[0].name) &  # filters for the strategic objective
            Q(tree_id=int(self.maplist[0].tree_id))  # filters for the specific tree
        )

    def get_context_data(self, **kwargs):
        # adding nodes into the tree structure
        new_node = self.model(name='Workers')
        parent = self.model.objects.get(name='Actval Life System')
        # inserting the node
        # self.model.objects.insert_node(new_node, parent, position='last-child', save=True)
        # new_node.insert_at(parent, position='first-child', save=True)
        # self.model.objects.filter(name__in=['code quality','Wonderful Programmer','Timely deilivery']).delete()
        # self.model.objects.filter(name__in=['Timely Deilivery']).delete()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['levels'] = self.maplist
        context['levelset'] = self.model.objects.filter(
            tree_id__exact=int(self.tree_pk))  # for querying the distinct tree
        context['dataset'] = self.model.objects.all()
        return context


class LevelStructureCreateView(BSModalCreateView, generic.FormView):
    template_name = 'levels/create_level.html'
    form_class = LevelStructureForm
    success_message = 'Success: Data was created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        print(form)
        return redirect(reverse("levelStructureIndex", kwargs={
            'maplist': form.instance.maplist
        }))


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
        print(weights)
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
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("levelIndex", kwargs={
            'maplist': form.instance.maplist
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
    maplist_id = request.GET.get('maplist_data')  # collect the maplist_id
    context['levelset'] = Level.objects.filter(maplist_id=maplist_id)  # match the collected maplist_id and maplist
    # then present the data for that specific maplist
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


def add_weights(request, pk):
    context = {}
    template_name = 'levels/add_weights.html'
    context['levels'] = InputData.objects.all()
    form = KPIWeightForm(request.POST or None)
    # the computation algorithm for weight allocation in the specific levels
    if form.is_valid():
        # form.save()
        for index in range(0, 1):
            '''
            Ensure index can be picked dynamically.
            '''
            index = pk
            # form processing
            if KPIWeightings.objects.filter(
                    ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=index) & Q(
                        created_at__gt=F('created_at') - timezone.timedelta(seconds=3))):
                if request.POST.get('weight') == None:
                    each_weight = 0
                else:
                    each_weight = request.POST.get('weight')
                context['total_weight_0'] = KPIWeightings.objects.filter(
                    ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=index) & Q(
                        created_at__gt=F('created_at') - timezone.timedelta(seconds=3))).aggregate(
                    Sum('weight'))
                context['data'] = KPIWeightings.objects.filter(
                    ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=index) & Q(
                        created_at__gt=F('created_at') - timezone.timedelta(seconds=3))).values(
                    "content_id__name").annotate(
                    Count("content_id"),
                    val=F('weight'), sum=Sum('weight'),
                    content=F('content'),
                    final_weight=F(
                        'final_weight')).last()
                dataset = KPIWeightings.objects.filter(
                    ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=index) & Q(
                        created_at__gt=F('created_at') - timezone.timedelta(seconds=3))).values(
                    "content_id__name").annotate(Count("content_id"))
                weight_set = []
                for indexes in range(0, len(dataset)):
                    weight_set.insert(indexes, KPIWeightings.objects.filter(
                        content_id__name=dataset[indexes]['content_id__name']).values('weight').annotate(
                        content=F('content_id__name'), contents=F('content_id')).order_by(
                        'created_at').last())
                context['weightings'] = weight_set
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
                # if request.method == 'POST':
                # form = KPIWeightForm(request.POST or None
                keyset = []
                for key, val in values.contents.items():
                    if val == int(request.POST.get('content')):
                        keyset.append(int(key))
                context['calculated_weight'] = (int(each_weight) / context['total_weight_0'][
                    'weight__sum']) * 100
                form.instance.final_weight = percentages[keyset[0]]
        # weight filters
        form.save()

    # environment_variables
    context['strategic_objectives'] = int(request.POST.get('content'))
    print(context['strategic_objectives'])
    '''
    Ensure the weight_listing is sorted dynamically
    '''
    # form = KPIWeightForm()
    context['form'] = form
    if pk == 0:
        weight_list = KPIWeightings.objects.filter(
            ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
        weight_filter = WeightFilter(request.GET, queryset=weight_list)
        context['filter'] = weight_filter
    if pk == 1:
        weight_list_1 = KPIWeightings.objects.filter(
            ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
        weight_filter = WeightFilter(request.GET, queryset=weight_list_1)
        context['filter_1'] = weight_filter
    if pk == 2:
        weight_list_2 = KPIWeightings.objects.filter(
            ~Q(content_id__levelset_id=None) & Q(content_id__number_of_levels__exact=pk)).order_by('-created_at')
        weight_filter = WeightFilter(request.GET, queryset=weight_list_2)
        context['filter_2'] = weight_filter
    return render(request, template_name, context)
    #
