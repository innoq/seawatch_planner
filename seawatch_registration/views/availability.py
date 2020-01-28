import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from seawatch_registration.mixins import HasProfileMixin, RegistrationStepOrderMixin
from seawatch_registration.models import Availability, Profile
from seawatch_registration.widgets import CustomDateInput


class CreateView(LoginRequiredMixin, HasProfileMixin, generic.CreateView):
    model = Availability
    fields = ['start_date', 'end_date', 'comment']
    nav_item = 'availabilities'
    submit_button = _('Add')
    success_url = reverse_lazy('availability_list')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        return super(CreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = CustomDateInput()
        form.fields['end_date'].widget = CustomDateInput()
        return form


class AvailabilityListView(LoginRequiredMixin,
                           HasProfileMixin,
                           RegistrationStepOrderMixin,
                           generic.FormView):
    nav_item = 'availabilities'
    title = _('Availabilities')
    success_alert = _('Available dates have been saved!')
    submit_button = _('Save')
    template_name = './seawatch_registration/availability_list.html'
    success_url = reverse_lazy('availability_list')

    AvailableDatesFormset = inlineformset_factory(
        Profile,
        Availability,
        fields=('start_date', 'end_date', 'comment'),
        widgets={
            'start_date': CustomDateInput,
            'end_date': CustomDateInput},
        extra=0, max_num=4, min_num=1,
        can_delete=True)

    def get_form_class(self):
        return self.AvailableDatesFormset

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'instance': self.request.user.profile
        }

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'formset': self.get_form()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
