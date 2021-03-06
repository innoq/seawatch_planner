from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, EmailField
from django.urls import reverse_lazy
from django.views import generic

from seawatch_registration.mixins import RegistrationStepOrderMixin


class SignupForm(UserCreationForm):
    email = EmailField(max_length=100, required=True)
    first_name = CharField(max_length=100, label='First name', required=True)
    last_name = CharField(max_length=100, label='Last name', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


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
