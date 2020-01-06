from django.views import generic
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse_lazy

from missions.models import Ship


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Ship
    fields = ['name']
    nav_item = 'ships'
    permission_required = 'missions.add_ship'
    success_url = reverse_lazy('ship_list')


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Ship
    fields = ['name']
    nav_item = 'ships'
    permission_required = 'missions.change_ship'
    success_url = reverse_lazy('ship_list')


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Ship
    ordering = 'name'
    paginate_by = 10
    nav_item = 'ships'
    permission_required = 'missions.view_ship'


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Ship
    nav_item = 'ships'
    success_url = reverse_lazy('ship_list')
    permission_required = 'missions.delete_ship'
