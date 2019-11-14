from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from seawatch_registration.models import Profile
from seawatch_registration.tests.views import util


class TestEditProfielView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.url_edit_profile = reverse('edit_profile')

    def test_views__edit_profile__get__should_get_403_when_no_profile_exists(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_edit_profile)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__edit_profile__get__should_get_profile_form_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_edit_profile)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_views__edit_profile__post__should_edit_profile_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_edit_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch',
                                     'date_of_birth': date.today(),
                                     'place_of_birth': 'New York',
                                     'country_of_birth': 'United States of America',
                                     'gender': 'm',
                                     'needs_schengen_visa': False,
                                     'phone': '0987654321'},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, reverse('show_profile'))
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0987654321')

    def test_views__edit_profile__post__should_not_edit_profile_when_required_data_is_missing(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_edit_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0123456789')