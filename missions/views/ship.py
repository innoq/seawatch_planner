import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy

from missions.models import Ship


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Ship
    fields = ['name']
    nav_item = 'ships'
    permission_required = 'missions.add_ship'

    def get_success_url(self):
        return reverse('ship_list')


class DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    permission_required = 'missions.view_ship'
    model = Ship
    nav_item = 'ships'


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Ship
    paginate_by = 10
    nav_item = 'ships'
    permission_required = 'missions.view_ship'


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Ship
    nav_item = 'ships'
    success_url = reverse_lazy('ship_list')
    permission_required = 'missions.delete_ship'
