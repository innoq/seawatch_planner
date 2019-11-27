from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.profile_form import ProfileForm


class AddProfileView(LoginRequiredMixin, View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html', {'form': ProfileForm({'user': request.user}), 'view': self})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return render(request, 'profile.html', {'form': ProfileForm({'user': request.user}, request.POST),
                                                    'view': self})
        form.save()
        return redirect('add_skills')
