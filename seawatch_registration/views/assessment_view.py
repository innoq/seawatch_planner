from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic.base import View

from seawatch_registration.forms.assessment_form import AssessmentForm
from seawatch_registration.models import Profile, Answer, Document, Assessment


def get_data(profile: Profile, form: AssessmentForm):
    data = {'profile': profile,
            'form': form,
            }
    if profile.skills.exists():
        data['skills'] = profile.skills.all()
    if Answer.objects.filter(profile=profile).exists():
        data['answers'] = Answer.objects.filter(profile=profile).all()
    if Document.objects.filter(profile=profile).exists():
        data['documents'] = Document.objects.filter(profile=profile).all()
    return data


class AssessmentView(LoginRequiredMixin, View):

    def get(self, request, profile_id, *args, **kwargs):
        if profile_id is None or not Profile.objects.filter(pk=profile_id).exists():
            return HttpResponseNotFound()
        profile = Profile.objects.get(pk=profile_id)
        if not Assessment.objects.filter(profile=profile).exists():
            return HttpResponseNotFound()
        data = get_data(profile, AssessmentForm(profile_id=profile_id))
        return render(request, 'assessment.html', data)

    def post(self, request, profile_id, *args, **kwargs):
        if profile_id is None or not Profile.objects.filter(pk=profile_id).exists():
            return HttpResponseNotFound()
        profile = Profile.objects.get(pk=profile_id)
        if not Assessment.objects.filter(profile=profile).exists():
            return HttpResponseNotFound()
        form = AssessmentForm(request.POST, profile_id=profile_id)
        data = get_data(profile, form)
        if not form.is_valid():
            data['error'] = True
            return render(request, 'assessment.html', data)
        assessment = Assessment.objects.get(profile=profile)
        assessment.status = form.cleaned_data['assessment_status']
        assessment.comment = form.cleaned_data['comment']
        assessment.save()
        profile.approved_positions.set(form.cleaned_data['approved_positions'])

        data['success'] = True
        return render(request, 'assessment.html', data)
