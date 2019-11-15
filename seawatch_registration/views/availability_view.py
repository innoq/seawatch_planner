from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import render, redirect

from seawatch_registration.models import Profile, Availability
from seawatch_registration.forms.availability_form import AvailabilityFormset

class AvailabilityView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def __init__(self):
        super(AvailabilityView, self).__init__()
        self.title = 'Availability'
        self.success_alert = 'Available Dates successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        formset = AvailabilityFormset(queryset=Availability.objects.filter(profile=profile))
        return render(request,
                        'availability.html',
                        {'formset': formset,
                        'title': self.title,
                        'success_alert': self.success_alert,
                        'submit_button': self.submit_button
                        })

    def post(self, request, *args, **kwargs):

        print(request.POST.values)

        profile = Profile.objects.get(user=request.user)
        #available_dates = Availability.objects.filter(profile=profile)
        # form = AvailabilityForm(request.POST)
        formset = AvailabilityFormset(request.POST)

        if not formset.is_valid():      
            print("Form is not valid")
            return render(request,
                            'availability.html',
                            {'formset': formset,
                            'error': request.POST,
                            'title': self.title,
                            'success_alert': self.success_alert,
                            'submit_button': self.submit_button
                            })


        print("form is valid")
        formset.save()
        return render(request,
                        'availability.html',
                        {'formset': formset,
                        'title': self.title,
                        'success_alert': self.success_alert,
                        'submit_button': self.submit_button
                        })


    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()