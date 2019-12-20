import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import CheckboxSelectMultiple
from django.urls import reverse_lazy

from seawatch_registration.mixins import (ModelFormWidgetMixin,
                                          RedirectNextMixin)
from seawatch_registration.models import Profile


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, ModelFormWidgetMixin,
                 RedirectNextMixin, generic.UpdateView):

    nav_item = 'positions'
    model = Profile
    fields = ['requested_positions']
    template_name = 'form.html'
    submit_button = 'Save'
    error_message = 'Error your selection was not saved! Select at least one position.'
    success_message = 'Your requested positions are successfully saved!'
    title = 'Requested Positions'
    widgets = {
        'requested_positions': CheckboxSelectMultiple,
    }
    success_url = reverse_lazy('question_answer')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
