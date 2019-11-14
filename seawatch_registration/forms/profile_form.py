from django.forms import ModelForm, HiddenInput

from seawatch_registration.models import Profile


class ProfileForm(ModelForm):
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
        widgets = {'user': HiddenInput()}