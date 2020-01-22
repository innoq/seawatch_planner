from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.mixins import HasProfileMixin, RegistrationStepOrderMixin
from seawatch_registration.models import Document, Profile


class UserOwnsDocuments(UserPassesTestMixin):
    def test_func(self):
        return (Profile.objects.filter(user=self.request.user).exists() and
                Document.objects.filter(
                    profile=self.request.user.profile,
                    id=self.kwargs.get('document_id')).exists())


class DocumentCreateView(LoginRequiredMixin,
                         RegistrationStepOrderMixin,
                         HasProfileMixin, generic.CreateView):
    model = Document
    nav_item = 'documents'
    title = _('Add Documents')
    success_alert = _('Document has been saved.')
    submit_button = _('Upload document')
    template_name = 'form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('document_list')
    can_be_skipped = True
    skip_button_text = _('Provide documents later')

    def post(self, request, *args, **kwargs):
        if 'skip' in request.POST:
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class ListView(LoginRequiredMixin, HasProfileMixin, generic.ListView):
    model = Document
    template_name = './seawatch_registration/document_list.html'
    context_object_name = 'documents'
    paginate_by = 5
    nav_item = 'documents'

    def get_queryset(self):
        return Document.objects.filter(profile=self.request.user.profile).order_by('id')


class DeleteView(LoginRequiredMixin, UserOwnsDocuments, generic.DeleteView):
    model = Document
    nav_item = 'documents'
    title = _('Delete Document')
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('document_list')
    pk_url_kwarg = 'document_id'


class UpdateView(LoginRequiredMixin, UserOwnsDocuments, generic.UpdateView):
    model = Document
    nav_item = 'documents'
    title = _('Edit documents')
    success_alert = _('Document has been updated.')
    submit_button = _('Save')
    template_name = 'form.html'
    form_class = DocumentForm
    success_url = reverse_lazy('document_list')
    pk_url_kwarg = 'document_id'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class GetDocumentAttachment(LoginRequiredMixin, UserOwnsDocuments, generic.View):

    def get(self, request, document_id, **kwargs):
        """ Ignore the filename since it is unsanitized user input and
        cannot be trusted. The mixin checked whether the user owns the file or
        not."""
        document = get_object_or_404(Document, id=document_id)
        with open(document.file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' % document.file.name
            return response
