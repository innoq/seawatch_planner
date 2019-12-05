import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect

from seawatch_registration.forms.profile_form import ProfileForm
from seawatch_registration.models import Profile


class CreateView(LoginRequiredMixin, generic.View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        return render(request, './seawatch_registration/profile.html', {'form': ProfileForm({'user': request.user}), 'view': self})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return render(request, './seawatch_registration/profile.html', {'form': ProfileForm({'user': request.user}, request.POST),
                                                    'view': self})
        form.save()
        return redirect('skill_update')


class DetailView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        return render(request, './seawatch_registration/profile_detail.html', {'profile': profile, 'view': self})

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    nav_item = 'profile'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, './seawatch_registration/profile.html', {'form': form, 'view': self})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(request.POST or None, instance=profile)
        if not form.is_valid():
            return render(request, './seawatch_registration/profile.html', {'form': form, 'view': self})
        form.save()
        redirect_to = request.GET.get('next')
        if redirect_to:
            return redirect(redirect_to)

        return redirect('profile_detail')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
