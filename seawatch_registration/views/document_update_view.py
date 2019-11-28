from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.models import Profile, Document


class DocumentUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'documents'
    title = 'Edit Document'
    success_alert = 'Document is successfully updated!'
    submit_button = 'Save'

    def get(self, request, document_id, *args, **kwargs):
        profile = request.user.profile
        document = get_object_or_404(Document, pk=document_id, profile=profile)
        return render(request, 'form.html', {'form': DocumentForm(user=request.user, instance=document),
                                             'view': self})

    def post(self, request, document_id, *args, **kwargs):
        profile = request.user.profile
        document = get_object_or_404(Document, pk=document_id, profile=profile)
        form = DocumentForm(request.POST, request.FILES, user=request.user, instance=document)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'view': self})
        form.save()
        return redirect('document_list')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
