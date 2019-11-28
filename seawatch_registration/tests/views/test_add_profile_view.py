from datetime import date

from django.urls import reverse

from seawatch_registration.models import Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestAddProfileView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('profile_create'), login_required=True)

    def test_views__profile_create__post__should_redirect_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url,
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

    def test_views__profile_create__post__should_not_redirect_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(Profile.objects.all().count(), 0)
