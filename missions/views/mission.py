from django import forms
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.views import generic

from missions.models import Mission, Assignment
from seawatch_registration.models import Profile
from seawatch_registration.widgets import DateInput


class SideBySideFrom(forms.Form):
    assignment_pk = forms.CharField(required=True)
    assignee_pk = forms.CharField(required=True)


class SideBySideView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'missions/mission_assignment_editor.html'
    permission_required = 'missions.view_mission'
    form_class = SideBySideFrom

    def get_success_url(self):
        return reverse('side_by_side_view', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        candidates = Profile.objects.all()
        mission = Mission.objects.get(pk=self.kwargs.get('pk'))
        return {
            **super().get_context_data(**kwargs),
            'mission': mission,
            'candidates': candidates
        }

    def form_valid(self, form):
        assignment = Assignment.objects.get(pk=form.cleaned_data['assignment_pk'])
        assignee = Profile.objects.get(pk=form.cleaned_data['assignee_pk'])
        mission_id = assignment.mission.pk

        assignee.user.assignments.filter(mission_id=mission_id).update(user=None)
        assignment.user = assignee.user
        assignment.save()

        return super().form_valid(form)


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Mission
    ordering = 'id'
    paginate_by = 100  # if pagination is desired
    nav_item = 'missions'
    permission_required = 'missions.view_mission'


class DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Mission
    nav_item = 'missions'
    permission_required = 'missions.view_mission'


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Mission
    fields = ['name', 'start_date', 'end_date', 'ship']
    nav_item = 'missions'
    permission_required = 'missions.add_mission'

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
    permission_required = 'missions.delete_mission'


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Mission
    nav_item = 'missions'
    fields = ['name', 'start_date', 'end_date', 'ship']
    success_url = reverse_lazy('mission_list')
    permission_required = 'missions.change_mission'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = DateInput()
        form.fields['end_date'].widget = DateInput()
        return form
