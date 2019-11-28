from django.urls import reverse

from seawatch_registration.models import Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestShowProfileView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('profile_detail'), login_required=True, profile_required=True)

    def test_views__profile_detail__get__should_render_with_profile_detail_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile-detail.html')
