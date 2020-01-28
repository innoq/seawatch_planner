from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.views import generic

from seawatch_registration.mixins import (ModelFormWidgetMixin,
                                          HasProfileMixin, RegistrationStepOrderMixin)
from seawatch_registration.models import Profile


class PositionUpdateView(LoginRequiredMixin, RegistrationStepOrderMixin, HasProfileMixin, ModelFormWidgetMixin,
                         generic.UpdateView):
    nav_item = 'positions'
    model = Profile
    fields = ['requested_positions']
    template_name = 'form.html'
    submit_button = _('Save')
    error_message = _('Your selection could not be saved. Please select at least one position.')
    success_message = _('Your requested positions have been saved.')
    title = _('Requested Positions')
    widgets = {
        'requested_positions': CheckboxSelectMultiple,
    }

    def get_object(self, **kwargs):
        return Profile.objects.get(user=self.request.user)
