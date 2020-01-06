from django.urls import reverse

from seawatch_registration.models import Position, Profile
from seawatch_registration.tests.views.test_base import TestBases


class TestAddRequestedPositionsView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('requested_position_update'), login_required=True, profile_required=True)

    def test_views__add_requested_positions__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_requested_positions__get__should_show_selected_positions_when_requested_positions_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.requested_positions.add(Position.objects.filter().first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_requested_positions_')

    def test_views__add_requested_positions__post__should_render_error_when_no_position_is_selected(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        position = Position.objects.filter().first()
        profile.requested_positions.add(position)
        profile.save()

        # Act
        response = self.client.post(self.url,
                                    {},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-danger')
        self.assertEquals(len(profile.skills.all()), 0)

    def test_views__add_requested_position__post__should_redirect_to_questions(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        position = Position.objects.filter().first()
        profile.save()

        # Act
        response = self.client.post(self.url,
                                    {'requested_positions': position.id},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, expected_url='/accounts/questions/edit/')
        self.assertEquals(len(profile.requested_positions.all()), 1)
