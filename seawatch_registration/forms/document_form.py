from django.forms import ModelForm, FileField, ModelChoiceField, HiddenInput

from seawatch_registration.models import DocumentType, Document, Profile


class DocumentForm(ModelForm):
    file = FileField()
    document_type = ModelChoiceField(queryset=DocumentType.objects.all(), initial=DocumentType.objects.all()[0:1])

    class Meta:
        model = Document
        fields = ('document_type', 'number', 'issuing_date', 'expiry_date', 'issuing_authority', 'issuing_place',
                  'issuing_country', 'file', 'profile')
        widgets = {'profile': HiddenInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')

        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['profile'] = ModelChoiceField(widget=HiddenInput(),
                                                        queryset=Profile.objects.filter(user=user),
                                                        initial=Profile.objects.get(user=user))
