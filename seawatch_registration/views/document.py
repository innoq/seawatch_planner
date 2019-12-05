import django.views.generic as generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404

from seawatch_registration.forms.document_form import DocumentForm
from seawatch_registration.models import Profile, Document


class CreateView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    nav_item = 'documents'
    title = 'Add Documents'
    success_alert = 'Document is successfully saved!'
    submit_button = 'Next'
    remove_input_type_date = True

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
        return redirect('requested_position_update')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
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


class ListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = './seawatch_registration/document_list.html'
    model = Document
    context_object_name = 'documents'
    paginate_by = 5
    nav_item = 'documents'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return Document.objects.filter(profile=profile).order_by('id')

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    nav_item = 'documents'
    title = 'Edit Document'
    success_alert = 'Document is successfully updated!'
    submit_button = 'Save'
    remove_input_type_date = True

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
