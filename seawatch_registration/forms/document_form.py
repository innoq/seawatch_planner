from django import forms

from seawatch_registration.models import Document, DocumentType, Profile
from seawatch_registration.widgets import DateInput


class DocumentForm(forms.ModelForm):
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all(),
                                           initial=DocumentType.objects.first())

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
        widgets = {'issuing_date': DateInput(),
                   'expiry_date': DateInput()}
