from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from seawatch_registration.models import Profile
from .forms import AssignmentForm
from .models import Mission, Assignment, Ship


class MissionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mission
    paginate_by = 100  # if pagination is desired
    nav_item = 'missions'
    permission_required = 'missions.can_view_missions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MissionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mission
    nav_item = 'missions'
    permission_required = 'missions.can_view_missions'
    

class MissionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mission
    fields = ['name', 'start_date', 'end_date', 'ship']
    nav_item = 'missions'
    permission_required = 'missions.can_create_missions'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.id})
    

class MissionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mission
    nav_item = 'missions'
    success_url = reverse_lazy('mission_list')
    permission_required = 'missions.can_delete_missions'


class ShipCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Ship
    fields = ['name']
    nav_item = 'ships'
    permission_required = 'missions.can_create_ships'

    def get_success_url(self):
        return reverse('ship_list')


class ShipDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'missions.can_view_ships'
    model = Ship
    nav_item = 'ships'


class ShipListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Ship
    paginate_by = 10
    nav_item = 'ships'
    permission_required = 'missions.can_view_ships'


class ShipDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Ship
    nav_item = 'ships'
    success_url = reverse_lazy('ship_list')
    permission_required = 'missions.can_delete_ships'


class AssignmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Assignment
    nav_item = 'missions'
    permission_required = 'missions.can_delete_assignments'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.mission.id})


class AssigneeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    initial = {'key': 'value'}
    template_name = 'missions/assignee_form.html'
    nav_item = 'missions'
    permission_required = 'missions.can_update_assignments'

    def get(self, request, *args, **kwargs):
        mission_id = kwargs.pop('mission__id')
        assigned_users = User.objects.filter(assignments__mission__id=mission_id)
        candidates = Profile.objects.exclude(user__in=assigned_users)
        return render(request, self.template_name, {'candidates': candidates, 'view': self})

    def post(self, request, *args, **kwargs):
        assignment_id = kwargs.pop('assignment__id')
        mission_id = kwargs.pop('mission__id')
        profile_id = request.POST['assignee']
        user = get_object_or_404(User, profile__pk=profile_id)
        assignment = Assignment.objects.get(pk=assignment_id)
        assignment.user = user
        assignment.save()
        return redirect(reverse('mission_detail', kwargs={'pk': mission_id}))


class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    form_class = AssignmentForm
    initial = {'key': 'value'}
    template_name = 'missions/assignment_form.html'
    nav_item = 'missions'
    permission_required = 'missions.can_create_assignments'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form,
                                                    'view': self})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        mission = get_object_or_404(Mission, pk=kwargs.pop('mission__id'))
        if form.is_valid():
            form.instance.mission_id = mission.id
            form.save()
            return redirect(reverse('mission_detail', kwargs={'pk': mission.id}))
        return render(request, self.template_name, {'form': form,
                                                    'view': self})
