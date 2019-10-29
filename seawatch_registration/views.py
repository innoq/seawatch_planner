from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms
from django.views.generic.base import View

from seawatch_registration.forms import ProfilePositionForm
from seawatch_registration.models import Profile, ProfilePosition, Position

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'user',
            'first_name',
            'last_name',
            'citizenship',
            'second_citizenship',
            'date_of_birth',
            'place_of_birth',
            'country_of_birth',
            'gender',
            'address',
            'needs_schengen_visa',
            'phone',
            'emergency_contact',
            'comments',
        )
        widgets = { 'user': forms.HiddenInput() }

def edit_profile(request):
    try:
        profile = Profile.objects.get(user = request.user)
    except Profile.DoesNotExist:
        return redirect('/accounts/add')

    form = ProfileForm(request.POST or None, instance = profile)

    if form.is_valid():
        form.save()
        return redirect('/admin')

    return render(request, 'profile.html', {'form': form})

def add_profile(request):
    form = ProfileForm({ 'user': request.user })

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/show/')

    return render(request, 'profile.html', {'form': form})

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1', 'password2')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/accounts/add')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def show_profile(request):
  profile = request.user.profile

  return render(request, 'show-profile.html', {'profile': profile})


class RequestedPositionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'position.html', {'form': ProfilePositionForm(user=request.user)})

    def post(self, request, *args, **kwargs):
        form = ProfilePositionForm(request.POST, user=request.user)
        if form.is_valid():
            profile = form.cleaned_data['profile']
            requested_positions = form.cleaned_data['requested_positions']
            for position in requested_positions:
                profile_position = ProfilePosition(profile=profile,
                                                   position=Position.objects.get(name=position),
                                                   requested=True,
                                                   approved=False)
                profile_position.save()
            return render(request,
                          'position.html',
                          {'form': ProfilePositionForm(user=request.user), 'success': True})
        return render(request, 'position.html', {'form': form, 'error': 'Choose at least one position.'})

    def test_func(self):
        try:
            Profile.objects.get(user=self.request.user)
            return True
        except ObjectDoesNotExist:
            return False
