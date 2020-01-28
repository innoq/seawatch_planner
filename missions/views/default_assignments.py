from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from missions.models import DefaultAssignment, Ship


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = DefaultAssignment
    fields = ['position', 'quantity']
    nav_item = 'ships'
    permission_required = 'missions.add_defaultassignment'

    def get_success_url(self):
        ship_id = self.kwargs.get('ship_id')
        return reverse('default_assignment_list', kwargs={'ship_id': ship_id})

    def form_valid(self, form):
        ship_id = self.kwargs.get('ship_id')
        if DefaultAssignment.objects.filter(position=form.cleaned_data['position'], ship=ship_id).exists():
            form.add_error('position', _('There is already a default assignment for this position for this ship!'))
            return self.form_invalid(form)

        form.instance.ship = get_object_or_404(Ship, pk=ship_id)
        return super(CreateView, self).form_valid(form)


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = DefaultAssignment
    fields = ['position', 'quantity']
    nav_item = 'ships'
    permission_required = 'missions.add_defaultassignment'

    def get_success_url(self):
        ship_id = self.kwargs.get('ship_id')
        return reverse('default_assignment_list', kwargs={'ship_id': ship_id})

    def form_valid(self, form):
        ship_id = self.kwargs.get('ship_id')
        form.instance.ship = get_object_or_404(Ship, pk=ship_id)
        return super(UpdateView, self).form_valid(form)


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = DefaultAssignment
    paginate_by = 10
    nav_item = 'ships'
    ordering = 'id'
    permission_required = 'missions.view_defaultassignment'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        ship_id = self.kwargs.get('ship_id')
        context['ship'] = get_object_or_404(Ship, pk=ship_id)
        return context

    def get_queryset(self):
        ship_id = self.kwargs.get('ship_id')
        return DefaultAssignment.objects.filter(ship__id=ship_id)


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = DefaultAssignment
    nav_item = 'ships'
    permission_required = 'missions.delete_defaultassignment'

    def get_success_url(self):
        ship_id = self.kwargs.get('ship_id')
        return reverse('default_assignment_list', kwargs={'ship_id': ship_id})

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        ship_id = self.kwargs.pop('ship_id')
        context['ship'] = get_object_or_404(Ship, pk=ship_id)
        return context
