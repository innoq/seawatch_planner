from django import forms

class AvailabilityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        available_dates = kwargs.pop('available_dates')
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        for date in available_dates:
            self.fields['date_start_' + str(date.pk)] = forms.DateField()
            self.fields['date_start_' + str(date.pk)].initial = date.start_date
            self.fields['date_end_' + str(date.pk)] = forms.DateField()
            self.fields['date_end_' + str(date.pk)].initial = date.end_date
            