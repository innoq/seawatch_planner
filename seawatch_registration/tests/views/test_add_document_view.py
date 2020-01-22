import tempfile
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from seawatch_registration.models import Document, DocumentType, Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestAddDocumentView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('document_create'), login_required=True, profile_required=True)

    def test_views__document_create__get__should_render_with_document_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_views__document_create__post__should_redirect_to_position_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")

        # Act
        response = self.client.post(self.url + '?initial_registration=yes',
                                    {'document_type': document_type.id,
                                     'number': '1234',
                                     'issuing_date': date.today(),
                                     'expiry_date': date.today(),
                                     'issuing_authority': 'New York City',
                                     'issuing_city': 'New York City',
                                     'issuing_country': 'United States of America',
                                     'profile': profile.id,
                                     'file': image},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, expected_url='/accounts/positions/edit/?initial_registration=yes')
        self.assertEquals(Document.objects.all().count(), 1)

    def test_views__document_create__post__should_render_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()

        # Act
        response = self.client.post(self.url,
                                    {'document_type': document_type.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertNotContains(response, 'alert-success')
        self.assertEquals(Document.objects.all().count(), 0)
