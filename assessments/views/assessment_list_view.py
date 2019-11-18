from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from assessments.models import Assessment
from seawatch_registration.models import Profile


class AssessmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'assessments.can_assess_profiles'
    template_name = 'assessment-list.html'
    model = Profile
    queryset = Profile.objects.filter(assessment__status='pending')
    context_object_name = 'profiles'
    paginate_by = 10
    ordering = ['id']
