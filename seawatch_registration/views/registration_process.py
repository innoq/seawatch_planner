from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from seawatch_registration.models import Profile
from assessments.models import Assessment


class View(LoginRequiredMixin, generic.TemplateView):
    nav_item = 'registration_process'
    title = 'Your registration status'
    success_alert = 'Your registration is completed!'
    submit_button = 'Confirm registration'
    template_name = 'seawatch_registration/registration_process.html'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        return {**super().get_context_data(**kwargs),
                'profile': profile,
                'answers': profile.answer_set.first(),
                'positions': profile.requested_positions.first(),
                'skills': profile.skills.first(),
                'availabilities': profile.availability_set.first(),
                'documents': profile.document_set.first()}

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        error_msg = 'Registration process not complete. Please provide all required data.'
        context = self.get_context_data(**kwargs)

        if 'confirmation' in request.POST:
            if all(context[required_data_name] for required_data_name in (
                    'answers', 'positions', 'skills', 'availabilities', 'documents')):
                Assessment.objects.create(profile=profile, status='pending')
                return render(request, self.template_name)
        else:
            # TODO: write matching error message
            error_msg = 'You have to agree to our terms and conditions.'

        return render(request, self.template_name, {**context, 'error': error_msg})
