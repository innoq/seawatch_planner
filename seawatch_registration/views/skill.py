from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View

from seawatch_registration.forms.skills_form import SkillsForm
from seawatch_registration.mixins import GetSuccessUrlFromUrlMixin
from seawatch_registration.models import Profile


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, GetSuccessUrlFromUrlMixin, View):
    nav_item = 'skills'
    title = 'Your Skills'
    success_alert = 'Skills are successfully saved!'
    submit_button = 'Next'
    error_message = 'Choose at least one Language'
    success_url = reverse_lazy('document_create')

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        return render(request, 'form.html', {'form': SkillsForm(profile=profile),
                                             'view': self})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = SkillsForm(request.POST, profile=profile)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'view': self
                                                 })
        languages = form.cleaned_data['languages']
        skills = form.cleaned_data['skills']
        profile.skills.clear()
        for skill in skills:
            profile.skills.add(skill)
        for language in languages:
            profile.skills.add(language)

        return redirect(self.get_success_url())

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
