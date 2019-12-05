from bootstrap_datepicker_plus import DatePickerInput as DatePicker
from django.forms.widgets import TextInput


class DateInput(TextInput):
    input_type = 'date'


class DatePickerInput(DatePicker):
    input_type = 'date'
