from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.models import Profile


class AddDocumentView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(AddDocumentView, self).__init__()
        self.title = 'Add Documents'
        self.success_alert = 'Document is successfully saved!'
        self.submit_button = 'Next'
        self.document_nav_class = 'active'

    def get(self, request, *args, **kwargs):
        return render(request, 'form.html', {'form': DocumentForm(user=request.user),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button,
                                             'document_nav_class': self.document_nav_class})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button,
                                                 'document_nav_class': self.profile_nav_class
                                                 })
        form.save()
        return redirect('add_requested_profile')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
