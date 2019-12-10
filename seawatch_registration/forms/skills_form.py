from django.forms import Form, ModelMultipleChoiceField, CheckboxSelectMultiple

from seawatch_registration.models import Profile, Skill


class SkillsForm(Form):
    class Meta:
        model = Profile

    languages = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                         queryset=Skill.objects.filter(group='lang'),
                                         required=True)
    skills = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                      queryset=Skill.objects.filter(group='other'),
                                      required=False)

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', '')
        super(SkillsForm, self).__init__(*args, **kwargs)

        if profile is not None:
            self.fields['skills'].initial = [p.pk for p in profile.skills.filter(group='other')]
            self.fields['languages'].initial = [p.pk for p in profile.skills.filter(group='lang')]
