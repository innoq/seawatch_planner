import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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
        answers = None
        positions = None
        skills = None
        availabilities = None
        error_msg = 'Registration Process not complete. Please provide all required data.'

        if profile:
            answers = Answer.objects.filter(profile=profile).first()
            positions = profile.requested_positions.first()
            skills = profile.skills.first()
            availabilities = Availability.objects.filter(profile=profile).first()

            print(request.POST)

            if answers and positions and skills and availabilities:

                if request.POST.get('confirmation'):
                    print('###### VALDID ########')
                    return render(request, 'seawatch_registration/registration_complete.html', {'view': self})

                # TODO: write matching error message
                error_msg = 'You have to agree to our terms and conditions.'

        return render(request, 'seawatch_registration/registration_process.html',
                      {'view': self,
                       'error': error_msg,
                       'profile': profile,
                       'answers': answers,
                       'positions': positions,
                       'skills': skills,
                       'availabilities': availabilities})

