from django import forms

from .models import Position, Profile, ProfilePosition


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
