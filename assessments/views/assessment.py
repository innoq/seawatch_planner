from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from assessments.forms.assessment_form import AssessmentForm
from assessments.models import Assessment
from seawatch_registration.models import Answer, Document


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    nav_item = 'assessment'
    permission_required = 'assessments.can_assess_profiles'
    template_name = 'assessment-list.html'
    queryset = Assessment.objects.filter(status='pending')
    paginate_by = 10
    ordering = ['id']
    context_object_name = 'pending_assessments'


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    nav_item = 'assessment'
    model = Assessment
    template_name = 'assessment-update.html'
    permission_required = 'assessments.can_assess_profiles'
    success_message = _('Updated assessment.')
    success_url = reverse_lazy('assessment_list')
    form_class = AssessmentForm

    def get_initial(self):
        return {'approved_positions': self.get_object().profile.approved_positions.all()}

    def get_context_data(self, **kwargs):
        profile = self.get_object().profile
        data = {}
        if profile.skills.exists():
            data['skills'] = profile.skills.all()
        if Answer.objects.filter(profile=profile).exists():
            data['answers'] = Answer.objects.filter(profile=profile).all()
        if Document.objects.filter(profile=profile).exists():
            data['documents'] = Document.objects.filter(profile=profile).all()
        return {
            **super().get_context_data(**kwargs),
            **data,
            'profile': profile
        }
