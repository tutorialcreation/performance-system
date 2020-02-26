import django
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .mixins import PassRequestMixin, DeleteMessageMixin, LoginAjaxMixin

DJANGO_VERSION = django.get_version().split('.')
DJANGO_MAJOR_VERSION = DJANGO_VERSION[0];
DJANGO_MINOR_VERSION = DJANGO_VERSION[1];


class BSModalCreateView(PassRequestMixin, SuccessMessageMixin,
                        generic.CreateView):
    pass


class BSModalUpdateView(PassRequestMixin, SuccessMessageMixin,
                        generic.UpdateView):
    pass


class BSModalReadView(generic.DetailView):
    pass


class BSModalDeleteView(DeleteMessageMixin, generic.DeleteView):
    pass
