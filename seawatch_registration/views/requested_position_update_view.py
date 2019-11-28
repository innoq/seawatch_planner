from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.requested_positions_form import RequestedPositionForm
from seawatch_registration.models import Profile


class RequestedPositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'positions'
    title = 'Add Requested Position'
    success_alert = 'Requested Positions are successfully saved!'
    submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        return render(request, 'form.html', {'form': RequestedPositionForm(user=request.user),
                                             'view': self})

    def post(self, request, *args, **kwargs):
        form = RequestedPositionForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': 'Choose at least one position.',
                                                 'view': self})
        profile = Profile.objects.get(user=request.user)
        requested_positions = form.cleaned_data['requested_positions']
        profile.requested_positions.clear()
        for position in requested_positions:
            profile.requested_positions.add(position)
        return redirect('question_update')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
