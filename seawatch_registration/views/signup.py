from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, HiddenInput
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import gettext as _

from seawatch_registration.mixins import RegistrationStepOrderMixin


class SignupForm(UserCreationForm):
    email = EmailField(max_length=100, required=True)
    username = CharField(widget=HiddenInput(), required=False)
    first_name = CharField(max_length=100, label='First name', required=True)
    last_name = CharField(max_length=100, label='Last name', required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(_('A user with this email address already exists.'))
        return self.cleaned_data['email']

    def clean_username(self):
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class SignupView(RegistrationStepOrderMixin, generic.FormView):
    nav_item = 'signup'
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('profile_create')
    starts_registration = True

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
