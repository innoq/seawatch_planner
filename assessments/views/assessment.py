import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render

from assessments.forms.assessment_form import AssessmentForm
from assessments.models import Assessment
from seawatch_registration.models import Profile, Answer, Document


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'assessments.can_assess_profiles'
    template_name = 'assessment-list.html'
    model = Profile
    queryset = Profile.objects.filter(assessment__status='pending')
    context_object_name = 'profiles'
    paginate_by = 10
    ordering = ['id']


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):

    permission_required = 'assessments.can_assess_profiles'

    def get(self, request, profile_id, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=profile_id)
        get_object_or_404(Assessment, profile=profile)
        data = self.get_data(profile, AssessmentForm(profile_id=profile_id))
        return render(request, 'assessment-update.html', data)

    def post(self, request, profile_id, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=profile_id)
        assessment = get_object_or_404(Assessment, profile=profile)
        form = AssessmentForm(request.POST, profile_id=profile_id)
        data = self.get_data(profile, form)
        if not form.is_valid():
            data['error'] = True
            return render(request, 'assessment-update.html', data)
        assessment.status = form.cleaned_data['assessment_status']
        assessment.comment = form.cleaned_data['comment']
        assessment.save()
        profile.approved_positions.set(form.cleaned_data['approved_positions'])

        data['success'] = True
        return render(request, 'assessment-update.html', data)

    @staticmethod
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
