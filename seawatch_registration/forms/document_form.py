from django import forms
from django.db.models import QuerySet
from django.utils.functional import lazy

from seawatch_registration.models import Document, DocumentType
from seawatch_registration.widgets import CustomDateInput


class DocumentForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(
        queryset=lazy(DocumentType.objects.all, QuerySet)(),
        initial=lazy(DocumentType.objects.first, DocumentType)())

    class Meta:
        model = Document
        fields = ['document_type',
                  'number',
                  'issuing_date',
                  'expiry_date',
                  'issuing_authority',
                  'issuing_place',
                  'issuing_country',
                  'file']
        widgets = {'issuing_date': CustomDateInput(),
                   'expiry_date': CustomDateInput()}
