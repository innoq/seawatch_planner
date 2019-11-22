from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from seawatch_registration.models import Document, Profile


class DocumentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'document-list.html'
    model = Document
    context_object_name = 'documents'
    paginate_by = 5

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Document.objects.filter(profile=profile).order_by('id')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['document_nav_class'] = 'active'
        return context
