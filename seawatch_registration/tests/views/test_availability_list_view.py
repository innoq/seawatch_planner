from django.urls import reverse

from seawatch_registration.models import Availability, Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestAvailabilityView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('availability_list'), login_required=True, profile_required=True)

    def test_views__availabilities__get__should_render_with_availability_list_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './seawatch_registration/availability_list.html')

    def test_views__availabilities__get__should_show_existing_availabilities(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        availability1 = Availability(
            profile=profile,
            start_date='2002-02-02',
            end_date='2010-10-10',
            comment='comment1')
        availability1.save()
        availability2 = Availability(
            profile=profile,
            start_date='2012-12-12',
            end_date='2013-01-01',
            comment='comment2')
        availability2.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './seawatch_registration/availability_list.html')
        self.assertContains(response, 'name="availability_set-TOTAL_FORMS" value="2"')
        self.assertContains(response, 'value="2002-02-02"')
        self.assertContains(response, 'value="2010-10-10"')
        self.assertContains(response, 'value="comment1"')
        self.assertContains(response, 'value="2012-12-12"')
        self.assertContains(response, 'value="2013-01-01"')
        self.assertContains(response, 'value="comment2"')
