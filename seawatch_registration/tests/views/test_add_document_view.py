import tempfile
from datetime import date
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings, Client
from django.urls import reverse

from seawatch_registration.models import Profile, DocumentType, Document
from seawatch_registration.tests.views import util


class TestAddDocumentView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.url_add_document = reverse('add_document')

    def test_views__add_document__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/document/add/')

    def test_views__add_document__get__should_return_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__add_document__get__should_render_with_document_html_when_profile_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_views__add_document__post__should_render_success_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")

        # Act
        response = self.client.post(self.url_add_document,
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
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(Document.objects.all().count(), 1)

    def test_views__add_document__post__should_render_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()

        # Act
        response = self.client.post(self.url_add_document,
                                    {'document_type': document_type.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertNotContains(response, 'alert-success')
        self.assertEquals(Document.objects.all().count(), 0)
