from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse

from seawatch_registration.models import Profile
from .forms import DocumentForm, ProfileForm, SignupForm


@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect(reverse('add_profile'))

    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect(reverse('show_profile'))

    return render(request, 'profile.html', {'form': form})


@login_required
def add_profile(request):
    form = ProfileForm({'user': request.user})

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/show/')

    return render(request, 'profile.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('add_profile'))
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def has_profile(user):
    return Profile.objects.filter(user=user).exists()


@login_required
def show_profile(request):
    if not has_profile(request.user):
        return redirect(reverse('add_profile'))
    profile = request.user.profile
    return render(request, 'show-profile.html', {'profile': profile})


@login_required
def add_document(request):
    if not has_profile(request.user):
        return redirect(reverse('add_profile'))
    form = DocumentForm(user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return render(request,
                          'document.html',
                          {'form': DocumentForm(user=request.user), 'success': True})
    return render(request, 'document.html', {'form': form})

