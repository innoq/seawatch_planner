import tempfile
from datetime import date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from seawatch_registration.models import Profile, DocumentType, Document
from seawatch_registration.tests.views.test_base import TestBases


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TestDeleteDocumentView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('document_delete', kwargs={'document_id': 1}),
                         login_required=True,
                         profile_required=True)

    def test_views__document_delete__get__should_get_403_when_document_doesnt_exist(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__document_delete__get__should_get_403_when_user_is_not_owner_of_document(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        user = User.objects.create_user(username='testuser', password='testuser')
        other_profile = Profile(pk=2,
                                user=user,
                                citizenship='Deutsch',
                                date_of_birth=date.today(),
                                place_of_birth='Hansestadt Hamburg',
                                country_of_birth='Deutschland',
                                gender='m',
                                needs_schengen_visa=False,
                                phone='0987654321')
        other_profile.save()
        document_type = DocumentType(name='TestType', group='other')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")
        document = Document(pk=1,
                            profile=other_profile,
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
        self.assertEquals(response.status_code, 403)

    def test_views__document_update__get__should_render_with_document_html_when_document_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        document_type = DocumentType(name='TestType', group='other')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")
        document = Document(pk=1,
                            profile=self.profile,
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
        self.assertTemplateUsed(response, 'confirm-delete.html')

    def test_views__document_delete__post__should_delete_document_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        profile.save()
        document_type = DocumentType(name='TestType', group='other')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")
        document = Document(pk=1,
                            profile=self.profile,
                            document_type=document_type,
                            number='123',
                            issuing_date=date.today(),
                            expiry_date=date.today(),
                            issuing_authority='New York City',
                            issuing_place='New York City',
                            issuing_country='United States of America',
                            file=image)
        document.save()

        # Act
        response = self.client.post(self.url, {}, user=self.user)

        # Assert
        self.assertRedirects(response, reverse('document_list'))
        self.assertEquals(Document.objects.all().count(), 0)

    def test_views__document_delete__post__should_get_403_when_user_is_not_owner_of_document(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        user = User.objects.create_user(username='testuser', password='testuser')
        other_profile = Profile(pk=2,
                                user=user,
                                citizenship='Deutsch',
                                date_of_birth=date.today(),
                                place_of_birth='Hansestadt Hamburg',
                                country_of_birth='Deutschland',
                                gender='m',
                                needs_schengen_visa=False,
                                phone='0987654321')
        other_profile.save()
        document_type = DocumentType(name='TestType', group='other')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")
        document = Document(pk=1,
                            profile=other_profile,
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
        response = self.client.post(self.url, {}, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)