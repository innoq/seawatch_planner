from django.contrib.auth.models import User
from django.forms import EmailField, CharField, ModelForm


class UserUpdateForm(ModelForm):

    email = EmailField(max_length=100, required=True)
    first_name = CharField(max_length=100, label='First name', required=True)
    last_name = CharField(max_length=100, label='Last name', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
