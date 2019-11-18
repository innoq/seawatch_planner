from django.forms import Form, ModelMultipleChoiceField, SelectMultiple, RadioSelect, ChoiceField, CharField, Textarea

from seawatch_registration.models import Position, Profile, Assessment


class AssessmentForm(Form):
    approved_positions = ModelMultipleChoiceField(widget=SelectMultiple,
                                                  queryset=Position.objects.all(),
                                                  required=False)
    assessment_status = ChoiceField(widget=RadioSelect, choices=Assessment.ASSESSMENT_STATUS)
    comment = CharField(widget=Textarea, max_length=2000, required=False)

    class Meta:
        model = Position

    def __init__(self, *args, **kwargs):
        profile_id = kwargs.pop('profile_id', '')

        super(AssessmentForm, self).__init__(*args, **kwargs)
        if Profile.objects.filter(pk=profile_id).exists():
            profile = Profile.objects.get(pk=profile_id)
            self.fields['approved_positions'].queryset = \
                profile.requested_positions
            self.fields['approved_positions'].initial = profile.approved_positions.all()
            self.fields['assessment_status'].initial = Assessment.objects.get(profile=profile).status
            self.fields['comment'].initial = Assessment.objects.get(profile=profile).comment
