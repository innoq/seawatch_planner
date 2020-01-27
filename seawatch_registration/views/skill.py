from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple, ModelForm
from django.views.generic import UpdateView

from seawatch_registration.mixins import HasProfileMixin, RegistrationStepOrderMixin
from seawatch_registration.models import Profile, Skill


class SkillsForm(ModelForm):
    languages = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                         queryset=Skill.objects.filter(group='lang'),
                                         required=True)
    skills = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                      queryset=Skill.objects.filter(group='other'),
                                      required=False)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        for category, skill_group in (('skills', 'other'), ('languages', 'lang')):
            self.fields[category].initial = instance.skills \
                .filter(group=skill_group) \
                .values_list('id', flat=True)

    def save(self, **kwargs):
        self.instance.skills.clear()
        for skill in (skill for skills in self.cleaned_data.values() for skill in skills):
            self.instance.skills.add(skill)
        return self.instance

    class Meta:
        model = Profile
        fields = ('languages', 'skills')


class SkillsUpdateView(LoginRequiredMixin, RegistrationStepOrderMixin, HasProfileMixin, UpdateView):
    nav_item = 'skills'
    title = 'Your Skills'
    success_alert = 'Skills are saved!'
    submit_button = 'Next'
    error_message = 'Choose at least one Language'
    form_class = SkillsForm
    template_name = 'form.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
