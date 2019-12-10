import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from assessments.models import Assessment
from seawatch_registration.models import Profile


class View(LoginRequiredMixin, generic.View):
    nav_item = 'registration_process'
    title = 'Your Registration Status'
    success_alert = 'Your registration is completed!'
    submit_button = 'Confirm Registration'
    answers = None
    positions = None
    skills = None
    availabilities = None
    documents = None

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user).first()

        if profile:
            self.answers = profile.answer_set.first()
            self.positions = profile.requested_positions.first()
            self.skills = profile.skills.first()
            self.availabilities = profile.availability_set.first()
            self.documents = profile.document_set.first()

        return render(request, 'seawatch_registration/registration_process.html',
                      {'view': self,
                       'profile': profile,
                       'answers': self.answers,
                       'positions': self.positions,
                       'skills': self.skills,
                       'availabilities': self.availabilities,
                       'documents': self.documents})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        error_msg = 'Registration Process not complete. Please provide all required data.'

        if profile:
            self.answers = profile.answer_set.first()
            self.positions = profile.requested_positions.first()
            self.skills = profile.skills.first()
            self.availabilities = profile.availability_set.first()
            self.documents = profile.document_set.first()

            print(request.POST)

            if self.answers and self.positions and self.skills and self.availabilities and self.documents:

                if request.POST.get('confirmation'):
                    new_assessment = Assessment(profile=profile, status='pending')
                    new_assessment.save()
                    return render(request, 'seawatch_registration/registration_complete.html', {'view': self})

                # TODO: write matching error message
                error_msg = 'You have to agree to our terms and conditions.'

        return render(request, 'seawatch_registration/registration_process.html',
                      {'view': self,
                       'error': error_msg,
                       'profile': profile,
                       'answers': self.answers,
                       'positions': self.positions,
                       'skills': self.skills,
                       'availabilities': self.availabilities,
                       'documents': self.documents})

