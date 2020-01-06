from django import forms
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.core import mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from missions.models import Assignment, Mission
from seawatch_registration.models import Profile


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Assignment
    nav_item = 'missions'
    permission_required = 'missions.delete_assignment'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.mission.id})


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['position']


class AssigneeForm(forms.Form):
    assignee = forms.CharField(
        required=True,
        error_messages={'required': 'Please select an assignee for the position.'})


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'missions/assignee_form.html'
    nav_item = 'missions'
    permission_required = 'missions.change_assignment'
    form_class = AssigneeForm

    def get_context_data(self, **kwargs):
        mission_id = self.kwargs.pop('mission__id')
        assignment_id = self.kwargs.pop('assignment__id')
        candidates = Profile.objects.exclude(
            Q(user__assignments__mission__id=mission_id) &
            ~Q(user__assignments__id=assignment_id))
        return {**super().get_context_data(**kwargs),
                'currently_selected': candidates.filter(user__assignments=assignment_id).first(),
                'candidates': candidates}

    def form_valid(self, form):
        assignment_id = self.kwargs.pop('assignment__id')
        mission_id = self.kwargs.pop('mission__id')
        profile_id = form.cleaned_data.get('assignee')
        user = get_object_or_404(User, profile__pk=profile_id)
        assignment = Assignment.objects.get(pk=assignment_id)
        assignment.user = user
        assignment.save()
        return redirect(reverse('mission_detail', kwargs={'pk': mission_id}))


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    form_class = AssignmentForm
    template_name = 'missions/assignment_form.html'
    nav_item = 'missions'
    permission_required = 'missions.add_assignment'

    def form_valid(self, form):
        mission = get_object_or_404(Mission, pk=self.kwargs.pop('mission__id'))
        form.instance.mission_id = mission.id
        form.save()
        return redirect(reverse('mission_detail', kwargs={'pk': mission.id}))


class EmailView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):
    nav_item = 'missions'
    permission_required = 'missions.add_assignment'
    template_name = './missions/assignment_confirm_mail.html'

    def get(self, request, *args, **kwargs):
        assignment = get_object_or_404(Assignment, pk=kwargs.pop('pk'), mission__id=kwargs.pop('mission__id'))
        return render(request, self.template_name, {'assignment': assignment})

    def post(self, request, *args, **kwargs):
        assignment = get_object_or_404(Assignment, pk=kwargs.pop('pk'), mission__id=kwargs.pop('mission__id'))
        name = assignment.user.first_name + " " + assignment.user.last_name

        subject = 'Sea-Watch.org: You have been assigned to a mission'
        message2 = render_to_string('missions/email_mission_assigned.html',
                                    {'name': name,
                                     'start_date': str(assignment.mission.start_date),
                                     'end_date': str(assignment.mission.end_date),
                                     'position': assignment.position.name,
                                     'ship_name': assignment.mission.ship.name,
                                     'stuff_name': 'Sea-Watch e.V.'})
        from_email = 'team@sea-watch.org'
        recipient_list = [assignment.user.email]

        mail.send_mail(subject, message2, from_email, recipient_list)
        assignment.email_sent = True
        assignment.save()
        return redirect(reverse('mission_detail', kwargs={'pk': assignment.mission.id}))
