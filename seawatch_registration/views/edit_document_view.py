from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.models import Profile, Document


class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(DocumentUpdateView, self).__init__()
        self.title = 'Edit Document'
        self.success_alert = 'Document is successfully updated!'
        self.submit_button = 'Save'
        self.document_nav_class = 'active'

    def get(self, request, document_id, *args, **kwargs):
        profile = request.user.profile
        document = get_object_or_404(Document, pk=document_id, profile=profile)
        return render(request, 'form.html', {'form': DocumentForm(user=request.user, instance=document),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button,
                                             'document_nav_class': self.document_nav_class})

    def post(self, request, document_id, *args, **kwargs):
        profile = request.user.profile
        document = get_object_or_404(Document, pk=document_id, profile=profile)
        form = DocumentForm(request.POST, request.FILES, user=request.user, instance=document)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button,
                                                 'document_nav_class': self.document_nav_class
                                                 })
        form.save()
        return redirect('document_list')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
