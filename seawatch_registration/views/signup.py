from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import View

from seawatch_registration.forms.signup_form import SignupForm
from seawatch_registration.tokens import account_activation_token


class SignupView(View):
    nav_item = 'signup'

    def get(self, request, *args, **kwargs):
        return render(request, './registration/signup.html', {'form': SignupForm(), 'view': self})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, './registration/signup.html', {'form': SignupForm(request.POST), 'view': self})
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('./seawatch_registration/email_signup_confirmation.html', {
            'name': user.first_name + ' ' + user.last_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


class ActivationView(View):
    def get(self, request, user_id, token):
        try:
            uid = force_text(urlsafe_base64_decode(user_id))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None or not account_activation_token.check_token(user, token):
            return HttpResponse('Activation link is invalid!')
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile_create')
