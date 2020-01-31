import functools
from urllib.parse import urlencode

from django import forms
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.core import mail
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from missions.models import Assignment, Mission
from seawatch_registration.models import Profile, Position
from seawatch_registration.widgets import CustomDateInput


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    class AssignmentFilterForm(forms.Form):
        name = forms.CharField(required=False, help_text=_('Searches first and last name case-insensitive.'))
        start_date = forms.DateField(widget=CustomDateInput(), required=False)
        end_date = forms.DateField(widget=CustomDateInput(), required=False)
        position = forms.ModelChoiceField(queryset=Position.objects.all(),
                                          to_field_name='name',
                                          required=False)

    class AssignmentAssigneeForm(forms.ModelForm):
        assignee = forms.IntegerField(error_messages={'required': _('Please select an assignee for the position.')})

        def save(self, **kwargs):
            self.instance.user = User.objects.get(profile__pk=self.cleaned_data['assignee'])
            super().save(**kwargs)

        class Meta:
            model = Assignment
            fields = 'assignee',

    model = Assignment
    form_class = AssignmentAssigneeForm
    template_name = 'missions/assignee_form.html'
    nav_item = 'missions'
    permission_required = 'missions.change_assignment'
    pk_url_kwarg = 'assignment__id'

    def get_table_kwargs(self):
        return {'selected_user': self.object.user}

    def get_context_data(self, **kwargs):
        mission = get_object_or_404(Mission, id=(self.kwargs.pop('mission__id')))
        filter_form = self._get_filter_form()
        return {**super().get_context_data(**kwargs),
                'filter_form': filter_form,
                'profiles': self._get_candidate_profiles(**self.request.GET.dict()),
                'reset_url': self.get_default_filter_url_for_assignment(self.object),
                'mission': mission}

    @staticmethod
    def get_default_filter_url_for_assignment(assignment):
        url_params = '?' + '&'.join(f'{kwarg}={str(value)}' for kwarg, value in (
            ('position', assignment.position),
            ('start_date', assignment.mission.start_date),
            ('end_date', assignment.mission.end_date)
        ))
        return reverse('assignee', kwargs={'mission__id': assignment.mission.pk,
                                                     'assignment__id': assignment.pk}) + url_params

    def _get_filter_form(self):
        return self.AssignmentFilterForm(initial=self.request.GET.dict())

    def _get_candidate_profiles(self, *, start_date=None, end_date=None, position=None, name=None, **kwargs):
        filter_fields = ((('requested_positions__name', 'approved_positions__name'), position),
                         (('availability__start_date__lte',), start_date),
                         (('availability__end_date__gte',), end_date),
                         (('full_name__icontains',), name))
        return Profile.objects \
                   .annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name')) \
                   .distinct() \
                   .filter(Q(user__assignments=self.object) | self._to_cnf(filter_fields)) or Profile.objects.all()

    @staticmethod
    def _to_cnf(kwarg_tuples) -> Q:
        return functools.reduce(
            lambda p, q: p & q,
            (functools.reduce(lambda r, s: r | s, (Q(**{kwarg: value}) for kwarg in kwarg_list), Q())
             for (kwarg_list, value) in kwarg_tuples if value), Q())

    def post(self, request, *args, **kwargs):
        if request.POST.get('return_to_mission'):
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.kwargs.pop('mission__id')})


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Assignment
    fields = ['position']
    nav_item = 'missions'
    permission_required = 'missions.add_assignment'

    def form_valid(self, form):
        mission = get_object_or_404(Mission, pk=self.kwargs.pop('mission__id'))
        form.instance.mission_id = mission.id
        form.save()
        return redirect(reverse('mission_detail', kwargs={'pk': mission.id}))


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Assignment
    nav_item = 'missions'
    permission_required = 'missions.delete_assignment'

    def get_success_url(self):
        return reverse('mission_detail', kwargs={'pk': self.object.mission.id})


class EmailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Assignment
    context_object_name = 'assignment'
    nav_item = 'missions'
    permission_required = 'missions.add_assignment'
    template_name = './missions/assignment_confirm_mail.html'

    def post(self, request, *args, **kwargs):
        assignment = self.get_object()
        name = assignment.user.first_name + " " + assignment.user.last_name

        subject = _('Sea-Watch.org: You have been assigned to a mission')
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
