import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy

from missions.models import Mission
from seawatch_registration.widgets import DateInput


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Mission
    paginate_by = 100  # if pagination is desired
    nav_item = 'missions'
    permission_required = 'missions.can_view_missions'  # TODO: use djangos default permissions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Mission
    nav_item = 'missions'
    permission_required = 'missions.can_view_missions'  # TODO: use djangos default permissions


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Mission
    fields = ['name', 'start_date', 'end_date', 'ship']
    nav_item = 'missions'
    permission_required = 'missions.can_create_missions'  # TODO: use djangos default permissions

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = DateInput()
        form.fields['end_date'].widget = DateInput()
        return form


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Mission
    nav_item = 'missions'
    success_url = reverse_lazy('mission_list')
    permission_required = 'missions.can_delete_missions'  # TODO: use djangos default permissions
