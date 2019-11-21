from django import forms
from django.forms import inlineformset_factory, HiddenInput, DateInput
from seawatch_registration.models import Profile, Availability
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, HTML, ButtonHolder, Submit

import re

class AvailableDatesForm(forms.ModelForm):

    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter start date'
        })
    )

    end_date = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter end date'
        })
    )

    class Meta:
        model = Availability
        fields = ('start_date', 'end_date', 'profile',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('start_date'),
                Field('end_date'),
                Field('DELETE'),
                css_class='formset_row-{}'.format(formtag_prefix)
            )
        )

AvailabilityFormset = inlineformset_factory(Profile, Availability, form=AvailableDatesForm, extra=0, max_num = 4, min_num = 1, can_delete=True)
     