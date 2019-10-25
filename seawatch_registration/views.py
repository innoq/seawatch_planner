from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms
from seawatch_registration.models import Profile

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
