from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField


class SignupForm(UserCreationForm):
    email = EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
