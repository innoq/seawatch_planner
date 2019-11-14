from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.requested_positions_form import RequestedPositionForm
from seawatch_registration.models import Profile


class RequestedPositionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(RequestedPositionView, self).__init__()
        self.title = 'Add Requested Position'
        self.success_alert = 'Requested Positions are successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        return render(request, 'form.html', {'form': RequestedPositionForm(user=request.user),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button})

    def post(self, request, *args, **kwargs):
        form = RequestedPositionForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': 'Choose at least one position.',
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button
                                                 })
        profile = Profile.objects.get(user=request.user)
        requested_positions = form.cleaned_data['requested_positions']
        profile.requested_positions.clear()
        for position in requested_positions:
            profile.requested_positions.add(position)
        return redirect('questions')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
