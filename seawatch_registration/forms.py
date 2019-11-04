from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Position, Profile, ProfilePosition, DocumentType, Document


def positions_as_tuples():
    positions = list(Position.objects.all())
    result = set()
    for position in positions:
        result.add((position, position))
    return result


class ProfilePositionForm(forms.Form):
    listOfPositions = list(Position.objects.all())
    requested_positions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                    choices=positions_as_tuples())

    class Meta:
        model = ProfilePosition
        fields = ('profile', 'position', 'requested', 'approved')
        widgets = {'profile': forms.HiddenInput(), 'approved': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')

        super(ProfilePositionForm, self).__init__(*args, **kwargs)
        self.fields['profile'] = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                                        queryset=Profile.objects.filter(user=user),
                                                        initial=Profile.objects.get(user=user))


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
