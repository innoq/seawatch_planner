from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.base import View

from seawatch_registration.models import Profile, Document


class DeleteDocumentView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'documents'

    def get(self, request, document_id, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        document = get_object_or_404(Document, profile=profile, pk=document_id)

        return render(request, 'confirm-delete.html', {'title': 'Delete Document',
                                                       'object': document,
                                                       'view': self})

    def post(self, request, document_id, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        document = get_object_or_404(Document, profile=profile, pk=document_id)
        document.delete()
        return redirect('document_list')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
