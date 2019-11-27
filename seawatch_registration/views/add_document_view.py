from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.models import Profile


class AddDocumentView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'documents'
    title = 'Add Documents'
    success_alert = 'Document is successfully saved!'
    submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        return render(request, 'form.html', {'form': DocumentForm(user=request.user),
                                             'view': self})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'view': self
                                                 })
        form.save()
        return redirect('add_requested_profile')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
