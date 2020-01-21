from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from seawatch_registration.forms.user_update_form import UserUpdateForm
from seawatch_registration.mixins import RedirectNextMixin, HasProfileMixin
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


class DetailView(LoginRequiredMixin, HasProfileMixin, generic.DetailView):
    model = Profile
    nav_item = 'profile'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class UpdateView(LoginRequiredMixin, RedirectNextMixin, generic.TemplateView):
    nav_item = 'profile'
    submit_button = 'Save'
    template_name = './seawatch_registration/profile_update.html'
    success_url = reverse_lazy('profile_detail')

    def get_context_data(self, **kwargs):
        context = {**super().get_context_data(**kwargs),
                   'user_form': UserUpdateForm(instance=self.request.user)}
        if Profile.objects.filter(user=self.request.user).exists():
            profile_form = ProfileForm(instance=self.request.user.profile)
            context['profile_form'] = profile_form
        return context

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if Profile.objects.filter(user=self.request.user).exists():
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            profile_form.instance.user = self.request.user
            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save()
                user_form.save()
                return redirect(self.success_url)
            else:
                return render(request,
                              self.template_name,
                              {'user_form': user_form, 'profile_form': profile_form, 'view': self})
        else:
            if user_form.is_valid():
                user_form.save()
            return render(request,
                          self.template_name,
                          {'user_form': user_form, 'view': self})



