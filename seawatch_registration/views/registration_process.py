import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from seawatch_registration.models import Profile, Answer, Availability


class View(LoginRequiredMixin, generic.View):
    nav_item = 'registration_process'
    title = 'Your Registration Status'
    success_alert = 'Your registration is completed!'
    submit_button = 'Confirm Registration'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()
        answers = None
        positions = None
        skills = None
        availabilities = None

        if profile:
            answers = Answer.objects.filter(profile=profile).first()
            positions = profile.requested_positions.first()
            skills = profile.skills.first()
            availabilities = Availability.objects.filter(profile=profile).first()

        return render(request, 'seawatch_registration/registration_process.html',
                      {'view': self,
                       'profile': profile,
                       'answers': answers,
                       'positions': positions,
                       'skills': skills,
                       'availabilities': availabilities})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        print('####### post #######')

        return render(request, 'seawatch_registration/registration_complete.html', {'view': self})

