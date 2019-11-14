from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.skills_form import SkillsForm
from seawatch_registration.models import Profile


class AddSkillsView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(AddSkillsView, self).__init__()
        self.title = 'Add Skills'
        self.success_alert = 'Skills are successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        return render(request, 'form.html', {'form': SkillsForm(profile=profile),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = SkillsForm(request.POST, profile=profile)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': 'Choose at least one skill.',
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button
                                                 })
        languages = form.cleaned_data['languages']
        skills = form.cleaned_data['skills']
        profile.skills.clear()
        for skill in skills:
            profile.skills.add(skill)
        for language in languages:
            profile.skills.add(language)

        return redirect('add_document')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
