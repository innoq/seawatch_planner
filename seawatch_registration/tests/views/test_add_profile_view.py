from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from seawatch_registration.models import Profile


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.user.save()
        self.url_add_profile = reverse('add_profile')

    def test_views__add_profile__get__should_redirect_to_login_when_user_is_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_profile, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/add/')

    def test_views__add_profile__get__should_return_profile_form(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_profile, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_views__add_profile__post__should_redirect_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_add_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch',
                                     'date_of_birth': date.today(),
                                     'place_of_birth': 'New York',
                                     'country_of_birth': 'United States of America',
                                     'gender': 'm',
                                     'needs_schengen_visa': False,
                                     'phone': '0123456789'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Profile.objects.all().count(), 1)

    def test_views__add_profile__post__should_not_redirect_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_add_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(Profile.objects.all().count(), 0)
