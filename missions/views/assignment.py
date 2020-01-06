import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django_filters.views import FilterView
from django_filters import FilterSet
from django_tables2 import SingleTableMixin, RequestConfig, SingleTableView

from missions.forms import AssignmentForm
from missions.models import Assignment, Mission
from missions.tables.candidates import CandidatesTable
from seawatch_registration.models import Profile


class ProfileFilter(FilterSet):
    class Meta:
        model = Profile
        fields = ['id', 'user__first_name', 'user__last_name', 'requested_positions']


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Assignment
    nav_item = 'missions'
    permission_required = 'missions.delete_assignment'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.mission.id})


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'missions/assignee_form.html'
    nav_item = 'missions'
    permission_required = 'missions.change_assignment'
    table_class = CandidatesTable
    table_data = Profile.objects.all()
    model = Profile
    filterset_class = ProfileFilter

    def post(self, request, *args, **kwargs):

        mission_id = kwargs.pop('mission__id')

        assignment_id = kwargs.pop('assignment__id')
        profile_id = request.POST['assignee']
        if profile_id:
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
    permission_required = 'missions.add_assignment'

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


class EmailView(LoginRequiredMixin, PermissionRequiredMixin, View):
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
        message2 = render_to_string('missions/email_mission_assigned.html', {'name': name,
                                                                             'start_date': str(assignment.mission.start_date),
                                                                             'end_date': str(assignment.mission.end_date),
                                                                             'position': assignment.position.name,
                                                                             'ship_name': assignment.mission.ship.name,
                                                                             'stuff_name': 'Sea-Watch e.V.'
                                                                             })
        from_email = 'team@sea-watch.org'
        recipient_list = [assignment.user.email]

        mail.send_mail(subject, message2, from_email, recipient_list)
        assignment.email_sent = True
        assignment.save()
        return redirect(reverse('mission_detail', kwargs={'pk': assignment.mission.id}))
