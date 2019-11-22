from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.signup_form import SignupForm


class SignupView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html', {'form': SignupForm()})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': SignupForm(request.POST),
                                                   'signup_nav_class': 'active'})
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('add_profile')
