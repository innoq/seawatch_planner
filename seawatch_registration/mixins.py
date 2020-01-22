from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms.models import modelform_factory
from django.urls import reverse_lazy

from seawatch_registration.models import Profile


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class HasProfileMixin(UserPassesTestMixin):
    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class RegistrationStepOrderMixin:
    url_param = 'initial_registration'
    starts_registration = False

    def get_success_url(self):
        ''' Redirect to the next step during registration otherwise use the
        success_url provided by the view. Defaults to a redirect to itself. '''
        if self.url_param in self.request.GET or self.starts_registration:
            return f'{self._steps[self.__class__.__name__]}?{self.url_param}=yes'
        return self.success_url or self.request.path_info

    _steps = {
        'SignupView': reverse_lazy('profile_create'),
        'ProfileCreateView': reverse_lazy('skill_update'),
        'SkillsUpdateView': reverse_lazy('document_create'),
        'DocumentCreateView': reverse_lazy('requested_position_update'),
        'PositionUpdateView': reverse_lazy('question_answer'),
        'AnsweringQuestionsView': reverse_lazy('availability_list'),
        'AvailabilityListView': reverse_lazy('registration_process')
    }
