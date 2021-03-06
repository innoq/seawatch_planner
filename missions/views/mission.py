import django.views.generic as generic
from django import forms
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.urls import reverse, reverse_lazy

from missions.models import Mission, Assignment
from seawatch_registration.widgets import CustomDateInput


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Mission
    ordering = 'id'
    paginate_by = 100  # if pagination is desired
    nav_item = 'missions'
    permission_required = 'missions.view_mission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Mission
    nav_item = 'missions'
    permission_required = 'missions.view_mission'

    def get_context_data(self, **kwargs):
        mission = self.get_object()
        multiple_assignments_in_mission = \
            User.objects.annotate(assignment_cnt=Count('assignments', filter=Q(assignments__mission=mission)))\
                .filter(assignment_cnt__gt=1)

        multiple_assignments_in_different_missions = \
            User.objects.annotate(assignment_cnt=Count('assignments',
                                  filter=
                                  Q(assignments__mission__start_date__range=(mission.start_date, mission.end_date)) |
                                  Q(assignments__mission__end_date__range=(mission.start_date, mission.end_date)) |
                                  (Q(assignments__mission__start_date__lte=mission.start_date) &
                                   Q(assignments__mission__end_date__gte=mission.end_date)))
                                  - Count('assignments', filter=Q(assignments__mission=mission)) + 1) \
                .filter(assignment_cnt__gt=1)

        return {**super().get_context_data(**kwargs),
                'multiple_assigned_users': multiple_assignments_in_mission,
                'multiple_assigned_users_in_different_missions': multiple_assignments_in_different_missions}


class MissionCreateForm(forms.ModelForm):
    create_default_assignments = forms.BooleanField(
        required=False,
        initial=True)

    class Meta:
        model = Mission
        fields = ['name', 'start_date', 'end_date', 'ship', 'create_default_assignments']
        widgets = {
            'start_date': CustomDateInput(),
            'end_date': CustomDateInput()}


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Mission
    form_class = MissionCreateForm
    nav_item = 'missions'
    permission_required = 'missions.add_mission'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        mission = form.save()
        if form.cleaned_data['create_default_assignments']:
            self._create_default_assignments(mission)
        return super().form_valid(form)

    @staticmethod
    def _create_default_assignments(mission):
        for default_assignment in mission.ship.default_assignments.all():
            for _ in range(default_assignment.quantity):
                Assignment.objects.create(
                    mission=mission,
                    position=default_assignment.position)


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
        form.fields['start_date'].widget = CustomDateInput()
        form.fields['end_date'].widget = CustomDateInput()
        return form
