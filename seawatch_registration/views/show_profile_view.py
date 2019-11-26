from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic.base import View

from seawatch_registration.models import Profile


class ShowProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        return render(request, 'show-profile.html', {'profile': profile, 'view': self})

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
