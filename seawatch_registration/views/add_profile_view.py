from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.profile_form import ProfileForm


class AddProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html', {'form': ProfileForm({'user': request.user}),
                                                'profile_nav_class': 'active'})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return render(request, 'profile.html', {'form': ProfileForm({'user': request.user}, request.POST),
                                                    'profile_nav_class': 'active'})
        form.save()
        return redirect('add_skills')
