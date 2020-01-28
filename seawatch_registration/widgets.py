from django.forms.widgets import DateInput


class CustomDateInput(DateInput):
    input_type = 'date'
