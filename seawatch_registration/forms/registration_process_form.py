from django.forms import Form, HiddenInput

from seawatch_registration.models import Profile


class RegistrationProcessForm(Form):

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile')
        super(RegistrationProcessForm, self).__init__(*args, **kwargs)
