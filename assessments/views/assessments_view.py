from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View

from assessments.models import Assessment


class AssessmentOverviewView(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = 'assessments.can_assess_profiles'

    def get(self, request, *args, **kwargs):
        pending_assessments = Assessment.objects.filter(status='pending')
        pending_profiles = [a.profile for a in pending_assessments]
        return render(request, 'assessments.html', {'pending_profiles': pending_profiles})

