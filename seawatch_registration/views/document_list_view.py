from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from seawatch_registration.models import Document, Profile


class DocumentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'document-list.html'
    model = Document
    context_object_name = 'documents'
    paginate_by = 5
    nav_item = 'documents'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Document.objects.filter(profile=profile).order_by('id')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
