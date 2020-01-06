from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, EmailField


class SignupForm(UserCreationForm):
    email = EmailField(max_length=100, required=True)
    first_name = CharField(max_length=100, label='First name', required=True)
    last_name = CharField(max_length=100, label='Last name', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
