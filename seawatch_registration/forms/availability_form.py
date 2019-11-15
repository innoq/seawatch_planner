from django import forms
from django.forms import inlineformset_factory, HiddenInput, DateInput
from seawatch_registration.models import Profile, Availability

class AvailableDatesForm(forms.ModelForm):

    class Meta:
        model = Availability
        fields = ('start_date', 'end_date', 'profile')
        widgets = {'profile': HiddenInput(), 'start_date': DateInput()}

AvailabilityFormset = inlineformset_factory(Profile, Availability, form=AvailableDatesForm, extra=1, can_delete=True)
     