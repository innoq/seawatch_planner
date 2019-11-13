from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Position, Profile, DocumentType, Document, Skill


class RequestedPositionForm(forms.Form):
    requested_positions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                         queryset=Position.objects.all())

    class Meta:
        model = Position

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')

        super(RequestedPositionForm, self).__init__(*args, **kwargs)
        if Profile.objects.filter(user=user).exists():
            profile = Profile.objects.get(user=user)
            self.fields['requested_positions'].initial = \
                [p.pk for p in profile.requested_positions.all()]


class SkillsForm(forms.Form):
    class Meta:
        model = Profile

    languages = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                               queryset=Skill.objects.filter(group='lang'),
                                               required=False)
    skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Skill.objects.filter(group='other'),
                                            required=False)

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', '')
        super(SkillsForm, self).__init__(*args, **kwargs)

        if profile is not None:
            self.fields['skills'].initial = [p.pk for p in profile.skills.filter(group='other')]
            self.fields['languages'].initial = [p.pk for p in profile.skills.filter(group='lang')]


class DocumentForm(forms.ModelForm):
    file = forms.FileField()
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), initial=DocumentType.objects.all()[0:1])

    class Meta:
        model = Document
        fields = ('document_type', 'number', 'issuing_date', 'expiry_date', 'issuing_authority', 'issuing_place',
                  'issuing_country', 'file', 'profile')
        widgets = {'profile': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')

        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['profile'] = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                                        queryset=Profile.objects.filter(user=user),
                                                        initial=Profile.objects.get(user=user))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user',
            'first_name',
            'last_name',
            'citizenship',
            'second_citizenship',
            'date_of_birth',
            'place_of_birth',
            'country_of_birth',
            'gender',
            'address',
            'needs_schengen_visa',
            'phone',
            'emergency_contact',
            'comments',
        )
        widgets = {'user': forms.HiddenInput()}


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
