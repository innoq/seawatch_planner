import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View

from missions.forms import AssignmentForm
from missions.models import Assignment, Mission
from seawatch_registration.models import Profile


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Assignment
    nav_item = 'missions'
    permission_required = 'missions.can_delete_assignments'  # TODO: use djangos default permissions

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.mission.id})


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    initial = {'key': 'value'}
    template_name = 'missions/assignee_form.html'
    nav_item = 'missions'
    permission_required = 'missions.can_update_assignments'  # TODO: use djangos default permissions

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


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    form_class = AssignmentForm
    initial = {'key': 'value'}
    template_name = 'missions/assignment_form.html'
    nav_item = 'missions'
    permission_required = 'missions.can_create_assignments'  # TODO: use djangos default permissions

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
