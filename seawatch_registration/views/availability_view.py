from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import render, redirect

from seawatch_registration.models import Profile, Availability
from seawatch_registration.forms import AvailabilityForm

class AvailabilityView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def __init__(self):
        super(AvailabilityView, self).__init__()
        self.title = 'Availability'
        self.success_alert = 'Available Dates successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        available_dates = Availability.objects.filter(profile=profile)
        form = AvailabilityForm(available_dates=available_dates)
        return render(request,
                        'form.html',
                        {'form': form,
                        'title': self.title,
                        'success_alert': self.success_alert,
                        'submit_button': self.submit_button
                        })

    def post(self, request, *args, **kwargs):

        print(request)

        profile = Profile.objects.get(user=request.user)
        available_dates = Availability.objects.filter(profile=profile)
        form = AvailabilityForm(available_dates=available_dates)
        return render(request,
                        'form.html',
                        {'form': form,
                        'title': self.title,
                        'success_alert': self.success_alert,
                        'submit_button': self.submit_button
                        })


        # profile = Profile.objects.get(user=request.user)
        # available_dates = Availability.objects.filter(profile=profile)
        # form = AvailabilityForm(request.POST)
        # if not form.is_valid():
        #     return render(request,
        #                     'form.html',
        #                     {'form': form,
        #                     'title': self.title,
        #                     'success_alert': self.success_alert,
        #                     'submit_button': self.submit_button
        #                     })



    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()