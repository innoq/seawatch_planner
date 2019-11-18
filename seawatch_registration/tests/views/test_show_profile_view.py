from django.urls import reverse

from seawatch_registration.models import Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestShowProfileView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('show_profile'), login_required=True, profile_required=True)

    def test_views__show_profile__get__should_render_with_show_profile_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'show-profile.html')
