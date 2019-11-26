import tempfile
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from assessments.tests.test_base import TestBases
from seawatch_registration.models import Position, Document, DocumentType


class TestDocumentListView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('document_list'), login_required=True, profile_required=True)

    def test_views__document_list__get__should_show_text_when_no_documents_are_uploaded(self):
        # Arrange
        self.profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document-list.html')
        self.assertContains(response, "You doesn't have any documents uploaded yet!")

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_views__document_list__get__should_show_table_when_document_is_uploaded(self):
        # Arrange
        profile = self.profile
        position = Position.objects.all().first()
        profile.save()
        profile.requested_positions.set((position,))
        document_type = DocumentType(name='TestType', group='other')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")
        document = Document(profile=self.profile,
                            document_type=document_type,
                            number='123',
                            issuing_date=date.today(),
                            expiry_date=date.today(),
                            issuing_authority='New York City',
                            issuing_place='New York City',
                            issuing_country='United States of America',
                            file=image)
        document.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document-list.html')
        self.assertContains(response, self.td(document.pk))
        self.assertContains(response, self.td(document.document_type.name))
        self.assertContains(response, self.td(document.number))
        self.assertContains(response, self.td(document.issuing_date.strftime('%b. %d, %Y')))
        self.assertContains(response, self.td(document.expiry_date.strftime('%b. %d, %Y')))
        self.assertContains(response, self.td(document.issuing_authority))
        self.assertContains(response, self.td(document.issuing_place))
        self.assertContains(response, self.td(document.issuing_country))
        self.assertContains(response, self.td(document.file.name))
        self.assertContains(response, reverse('edit_document', kwargs={'document_id': document.pk}))
        self.assertContains(response, reverse('delete_document', kwargs={'document_id': document.pk}))

    @staticmethod
    def td(value):
        return '<td>' + str(value) + '</td>'
