from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import render, redirect

from seawatch_registration.models import Profile, Availability
from seawatch_registration.forms.availability_form import AvailableDatesFormset


class AvailabilityView(LoginRequiredMixin, UserPassesTestMixin, View):

    nav_item = 'availability'
    title = 'Add Availability'
    success_alert = 'Available Dates successfully saved!'
    submit_button = 'Next'
    template_name = 'availability.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        formset = AvailableDatesFormset(instance=profile)
        return render(request, self.template_name,
                        {'formset': formset,
                        'view': self
                        })

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        formset = AvailableDatesFormset(request.POST, instance=profile)
        if not formset.is_valid():      
            return render(request, self.template_name,
                            {'formset': formset,
                            'view': self,
                            'error': formset.errors,
                            })

        formset.save()
        #return redirect('show_profile')

        formset = AvailableDatesFormset(instance=profile)
        return render(request, self.template_name,
                        {'formset': formset,
                        'view': self
                        })

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
