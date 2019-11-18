from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View

from seawatch_registration.models import Assessment


class AssessmentOverviewView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pending_assessments = Assessment.objects.filter(status='pending')
        pending_profiles = [a.profile for a in pending_assessments]
        return render(request, 'assessments.html', {'pending_profiles': pending_profiles})

