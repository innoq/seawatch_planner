from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings

from seawatch_registration.models import Profile


class TestBases:
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    class TestBase(TestCase):

        def __init__(self, *args, **kwargs):
            super(TestBases.TestBase, self).__init__(*args, **kwargs)
            self.url = ''
            self.__login_required = False
            self.__profile_required = False

        def base_set_up(self, url, login_required=False, profile_required=False) -> None:
            self.client = Client()
            self.username = 'testuser1'
            self.password = '1X<ISRUkw+tuK'
            self.user = User.objects.create_user(username=self.username,
                                                 password=self.password,
                                                 first_name='Test',
                                                 last_name='User',
                                                 email="test@test.de")
            self.user.save()
            self.profile = Profile(id=1,
                                   user=self.user,
                                   citizenship='Deutsch',
                                   second_citizenship='American',
                                   date_of_birth=date.today(),
                                   place_of_birth='New York',
                                   country_of_birth='United States of America',
                                   gender='m',
                                   needs_schengen_visa=False,
                                   phone='0123456789')
            self.url = url
            self.__login_required = login_required
            self.__profile_required = profile_required

        def test__base__should_redirect_to_login_when_login_required_but_user_not_logged_in(self):
            if not self.__login_required:
                self.skipTest('login not required for ' + str(self.__class__))
            # Act
            response = self.client.get(self.url, user=self.user)

            # Assert
            self.assertRedirects(response, '/accounts/login/?next=' + self.url)

        def test__base__should_return_403_when_profile_required_but_doesnt_exist(self):
            if not self.__profile_required:
                self.skipTest('profile not required for ' + str(self.__class__))
            # Arrange
            self.client.login(username=self.username, password=self.password)

            # Act
            response = self.client.get(self.url, user=self.user)

            # Assert
            self.assertEquals(response.status_code, 403)
