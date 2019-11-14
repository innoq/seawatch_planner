from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from seawatch_registration.models import Profile, Position
from seawatch_registration.tests.views import util


class TestAddRequestedPositionsView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.url_add_positions = reverse('add_requested_profile')

    def test_views__add_requested_positions__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/position/')

    def test_views__add_requested_positions__get__should_get_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__add_requested_positions__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_requested_positions__get__should_show_selected_positions_when_requested_positions_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.requested_positions.add(Position.objects.filter().first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_requested_positions_')

    def test_views__add_requested_positions__post__should_render_error_when_no_position_is_selected(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        position = Position.objects.filter().first()
        profile.requested_positions.add(position)
        profile.save()

        # Act
        response = self.client.post(self.url_add_positions,
                                    {},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-danger')
        self.assertEquals(len(profile.skills.all()), 0)

    def test_views__add_requested_position__post__should_render_success_when_2_positions_are_set(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        position = Position.objects.filter().first()
        profile.save()

        # Act
        response = self.client.post(self.url_add_positions,
                                    {'requested_positions': position.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(len(profile.requested_positions.all()), 1)
