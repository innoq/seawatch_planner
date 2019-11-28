from django import forms
from django.forms import inlineformset_factory
from seawatch_registration.models import Profile, Availability
from . import widgets


#class AvailableDatesForm(forms.ModelForm):

    #start_date = forms.DateField(widget=widgets.DateInput)
    #end_date = forms.DateField(widget=widgets.DateInput)

AvailableDatesFormset = inlineformset_factory(Profile,
                                                Availability, 
                                                fields=('start_date', 'end_date'), 
                                                widgets={
                                                    'start_date': widgets.DateInput,
                                                    'end_date': widgets.DateInput},
                                                extra=0, max_num=4, min_num=1, 
                                                can_delete=True)
