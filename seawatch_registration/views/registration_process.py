from collections import namedtuple

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from assessments.models import Assessment

RegistrationStep = namedtuple('RegistrationStep',
                              'name view_url_edit optional completed')


class RegistrationForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        error_messages={'required': _('You have to agree to our terms and conditions.')},
        label=_('I agree that Seawatch can save and process my data.'))

    def clean(self):
        if not all(step.completed or step.optional for step in self.steps):
            raise forms.ValidationError(_('Registration process not complete. Please provide all required data.'))
        if self.user.profile.assessment_set.exists():
            raise forms.ValidationError(_('Already registered.'))

    def __init__(self, user=None, steps=None, **kwargs):
        self.steps = steps
        self.user = user
        super().__init__(**kwargs)


class View(LoginRequiredMixin, SuccessMessageMixin, generic.FormView):
    nav_item = 'registration_process'
    title = _('Your registration status')
    success_message = _('Thank you for finishing the registration.')
    success_url = reverse_lazy('registration_process')
    submit_button = _('Confirm registration')
    template_name = 'seawatch_registration/registration_process.html'
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                'steps': self._get_ordered_registration_steps()}

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(),
                'user': self.request.user,
                'steps': self._get_ordered_registration_steps()}

    def form_valid(self, form):
        Assessment.objects.create(profile=self.request.user.profile, status='pending')
        return super().form_valid(form)

    def _get_ordered_registration_steps(self):
        """ Summarises the **edit** views for each step in the correct order.
        The order during the creation of the profile, the skills, etc might differ. """
        profile = self.request.user.profile
        return [
            RegistrationStep(
                _('Profile'),
                'profile_update',
                optional=False,
                completed=profile is not None
            ),
            RegistrationStep(
                'Skills',
                'skill_update',
                optional=False,
                completed=profile.requested_positions.exists()
            ),
            RegistrationStep(
                'Documents',
                'document_list',
                optional=True,
                completed=profile.document_set.exists()
            ),
            RegistrationStep(
                'Requested Positions',
                'requested_position_update',
                optional=False,
                completed=profile.requested_positions.exists()
            ),
            RegistrationStep(
                'Questions',
                'question_answer',
                optional=False,
                completed=profile.answer_set.exists()
            ),
            RegistrationStep(
                'Availabilities',
                'availability_list',
                optional=False,
                completed=profile.availability_set.exists()
            ),
        ]
