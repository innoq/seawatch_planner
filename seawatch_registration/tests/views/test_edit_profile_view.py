from datetime import date

from django.urls import reverse

from seawatch_registration.models import Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestEditProfileView(TestBases.TestBase):

    def setUp(self):
        self.base_set_up(url=reverse('profile_update'), login_required=True, profile_required=True)

    def test_views__profile_update__get__should_get_profile_form_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './seawatch_registration/profile.html')

    def test_views__profile_updatee__post__should_update_profile_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url,
                                    {'user': self.user.id,
                                     'citizenship': 'Deutsch',
                                     'date_of_birth': date.today(),
                                     'place_of_birth': 'New York',
                                     'country_of_birth': 'United States of America',
                                     'gender': 'm',
                                     'needs_schengen_visa': False,
                                     'phone': '0987654321'},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, reverse('profile_detail'))
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0987654321')

    def test_views__profile_update__post__should_not_update_profile_when_required_data_is_missing(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url,
                                    {'user': self.user.id,
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0123456789')
