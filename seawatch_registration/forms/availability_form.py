from django import forms
from django.forms import modelformset_factory
from seawatch_registration.models import Profile, Availability

class AvailableDatesForm(forms.ModelForm):
    
    #Form for each period
    start_date = forms.DateField(
                    widget=forms.DateInput(),
                    required=True)
    end_date = forms.DateField(
                    widget=forms.DateInput(),
                    required=True)

    class Meta:
        model = Availability
        exclude = ()

AvailabilityFormset = modelformset_factory(Availability, form=AvailableDatesForm)
    

# class AvailabilityForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         profile = kwargs.pop('profile', None)
#         super(AvailabilityForm, self).__init__(*args, **kwargs)

#         AvailabilityFormset = modelformset_factory(Availability, fields=('start_date', 'end_date'), widgets={'start_date': forms.DateInput()})
        
#         if profile:
#             formset = AvailabilityFormset(queryset=Availability.objects.filter(profile=profile))



        # if available_dates:
        #     for date in available_dates:
        #         self.fields['date_start_' + str(date.pk)] = forms.DateField()
        #         self.fields['date_start_' + str(date.pk)].initial = date.start_date
        #         self.fields['date_end_' + str(date.pk)] = forms.DateField()
        #         self.fields['date_end_' + str(date.pk)].initial = date.end_date
        