from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.profile_form import ProfileForm
from seawatch_registration.models import Profile


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'profile.html', {'form': form, 'view': self})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST or None, instance=profile)
        if not form.is_valid():
            return render(request, 'profile.html', {'form': form, 'view': self})
        form.save()
        return redirect('profile_detail')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
