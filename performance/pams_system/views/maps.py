from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q, F
from django.shortcuts import render, redirect,reverse
from django.core.paginator import Paginator
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

from pams_system.forms.mapforms import MapTypeForm, MapListsForm
from pams_system.models.maps import MapType, MapList


class MapListCreateView(BSModalCreateView):
    template_name = 'maps/create_map.html'
    form_class = MapListsForm
    success_message = 'Success: Map List was created.'
    success_url = reverse_lazy('mapListIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("mapListIndex", kwargs={
            'maptype': form.instance.maptype_name
        }))


# in the class below we will initialize the form
# using this class based view
class MapListReadView(BSModalReadView):
    # assign the needed model
    model = MapList
    # assign the template name
    template_name = 'maps/read_map.html'
    # assign the needed form
    form_class = MapListsForm
    success_url = reverse_lazy('mapListIndex')


# This class based view is aimed at filtering the data
# based on the id and therefore we shall use the data from previous class
class MapListIndex(generic.ListView):
    model = MapList
    # queryset = MapList.maptypes.get_maptypes()
    template_name = 'maps/maplist_index.html'
    # paginate_by = 3

    def get_queryset(self):
        self.maptype_name = MapList.objects.filter(
            # we will filter the maplist and level
            Q(maptype_name_id__maptype_name=self.kwargs['maptype'])  # for distinctly identifying the maplis
        )
        return MapList.objects.filter(
            Q(maptype_name_id__maptype_name=self.maptype_name)  # filters for the maplist
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # maplist_list = MapList.objects.filter(
        #     Q(maptype_name_id__maptype_name=self.maptype_name))
        maplist_list = MapList.objects.all()
        paginator = Paginator(maplist_list, 3)
        page = self.request.GET.get('page')
        context['pagination'] = paginator.get_page(page)
        context['maplist_number'] = MapList.objects.count()
        # Add in the publisher
        context['maplist_levels'] = self.maptype_name
        return context

class MapListUpdateView(BSModalUpdateView):
    model = MapList
    template_name = 'maps/update_map.html'
    form_class = MapListsForm
    success_message = 'Success: Map List was updated.'
    success_url = reverse_lazy('mapListIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.save()
        return redirect(reverse("mapListIndex", kwargs={
            'maptype': form.instance.maptype_name
        }))

class MapListDeleteView(BSModalDeleteView):
    model = MapList
    template_name = 'maps/delete_map.html'
    success_message = 'Success: Map List was deleted.'
    success_url = reverse_lazy("mapListIndex")
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Update'
    #     return context
    #
    # def form_valid(self, form):
    #     form.save()
    #     return redirect(reverse("mapListIndex", kwargs={
    #         'maptype': form.instance.maptype_name
    #     }))
    def get_success_url(self):
        return reverse('mapListIndex', kwargs={
            'maptype': self.kwargs['pk']
        })


class MapTypeIndex(generic.ListView):
    model = MapType
    context_object_name = 'maps'
    template_name = 'maps/maptype_index.html'
    paginate_by = 3

    # def get(self, request, *args, **kwargs):
        # print(self.request.GET)
        # return redirect('mapTypeIndex')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        maptype_list = MapType.objects.all()
        paginator = Paginator(maptype_list,3)
        page = self.request.GET.get('page')
        context['pagination'] = paginator.get_page(page)
        return context

class MapTypeCreateView(BSModalCreateView):
    template_name = 'maps/create_map.html'
    form_class = MapTypeForm
    success_message = 'Success: Maptype was created.'
    success_url = reverse_lazy('mapTypeIndex')


class MaptypeUpdateView(BSModalUpdateView):
    model = MapType
    template_name = 'maps/update_map.html'
    form_class = MapTypeForm
    success_message = 'Success: Maptype was updated.'
    success_url = reverse_lazy('mapTypeIndex')


class MapTypeReadView(BSModalReadView):
    model = MapType
    template_name = 'maps/read_map.html'


class MapTypeDeleteView(BSModalDeleteView):
    model = MapType
    template_name = 'maps/delete_map.html'
    success_message = 'Success: Maptype was deleted.'
    success_url = reverse_lazy('mapTypeIndex')

