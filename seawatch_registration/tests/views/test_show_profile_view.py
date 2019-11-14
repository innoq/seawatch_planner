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
        self.url_show_profile = reverse('show_profile')

    def test_views__show_profile__get__should_render_with_show_profile_html_when_profile_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'show-profile.html')

    def test_views__show_profile__get__should_get_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__show_profile__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/show/')