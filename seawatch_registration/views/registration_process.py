import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect

from seawatch_registration.forms.registration_process_form import RegistrationProcessForm
from seawatch_registration.models import Profile


class View(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    nav_item = 'registration_process'
    title = 'Your Registration Process'
    success_alert = 'Your registration is completed!'
    submit_button = 'Confirm Registration'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)

        return render(request,
                      'form.html',
                      {'form': RegistrationProcessForm(profile=profile),
                       'view': self})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = RegistrationProcessForm(request.POST, profile=profile)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'view': self})

        return render(request, 'registration_complete.html', {'view': self})

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
