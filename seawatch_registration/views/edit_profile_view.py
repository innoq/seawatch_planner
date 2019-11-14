from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.profile_form import ProfileForm
from seawatch_registration.models import Profile


class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST or None, instance=profile)
        if not form.is_valid():
            return render(request, 'profile.html', {'form': form})
        form.save()
        return redirect('show_profile')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
