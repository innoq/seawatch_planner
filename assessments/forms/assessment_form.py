from django import forms

from assessments.models import Assessment
from seawatch_registration.models import Position


class AssessmentForm(forms.ModelForm):
    approved_positions = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,
                                                        queryset=Position.objects.all(),
                                                        required=False)
    status = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=Assessment.ASSESSMENT_STATUS)
    comment = forms.CharField(widget=forms.Textarea,
                              max_length=2000,
                              required=False)

    def save(self, **kwargs):
        assessment = self.instance
        assessment.status = self.cleaned_data['status']
        assessment.comment = self.cleaned_data['comment']
        assessment.profile.approved_positions.set(self.cleaned_data['approved_positions'])
        assessment.save()
        assessment.profile.save()
        return assessment

    class Meta:
        model = Assessment
        fields = ('approved_positions', 'status', 'comment')
