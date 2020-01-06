import django.views.generic as generic
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from seawatch_registration.mixins import RedirectNextMixin
from seawatch_registration.models import Profile
from seawatch_registration.widgets import DateInput, TextInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['citizenship',
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
        widgets = {'date_of_birth': DateInput(),
                   'citizenship': TextInput(attrs={'autofocus': True})}


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Profile
    nav_item = 'profile'
    template_name = './seawatch_registration/profile.html'
    success_url = reverse_lazy('skill_update')
    submit_button = 'Next'
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Profile
    nav_item = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, RedirectNextMixin, generic.UpdateView):
    navitem = 'profile'
    model = Profile
    template_name = './seawatch_registration/profile.html'
    success_url = reverse_lazy('profile_detail')
    submit_button = 'Save'
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
