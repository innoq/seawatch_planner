import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from seawatch_registration.mixins import ModelFormWidgetMixin, GetSuccessUrlFromUrlMixin
from seawatch_registration.models import Profile
from seawatch_registration.widgets import DateInput


class CreateView(LoginRequiredMixin, ModelFormWidgetMixin, generic.CreateView):
    model = Profile
    fields = ['first_name',
              'last_name',
              'citizenship',
              'second_citizenship',
              'date_of_birth',
              'place_of_birth',
              'country_of_birth',
              'gender',
              'address',
              'needs_schengen_visa',
              'phone',
              'emergency_contact',
              'comments']
    nav_item = 'profile'
    widgets = {'date_of_birth': DateInput()}
    template_name = './seawatch_registration/profile.html'
    success_url = reverse_lazy('skill_update')
    submit_button = 'Next'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateView, self).form_valid(form)


class DetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Profile
    nav_item = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, ModelFormWidgetMixin,
                 GetSuccessUrlFromUrlMixin, generic.UpdateView):
    navitem = 'profile'
    model = Profile
    fields = ['first_name',
              'last_name',
              'citizenship',
              'second_citizenship',
              'date_of_birth',
              'place_of_birth',
              'country_of_birth',
              'gender',
              'address',
              'needs_schengen_visa',
              'phone',
              'emergency_contact',
              'comments']
    template_name = './seawatch_registration/profile.html'
    success_url = reverse_lazy('profile_detail')
    submit_button = 'Save'
    widgets = {'date_of_birth': DateInput()}

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
