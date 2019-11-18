from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase, Client

from seawatch_registration.models import Profile


class TestBase(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        self.url = ''
        self.__login_required = False
        self.__profile_required = False
        # Kludge alert: We want this class to carry test cases without being run
        # by the unit test framework, so the `run' method is overridden to do
        # nothing.  But in order for sub-classes to be able to do something when
        # run is invoked, the constructor will rebind `run' from TestCase.
        if self.__class__ != TestBase:
            # Rebind `run' from the parent class.
            self.run = TestCase.run.__get__(self, self.__class__)
        else:
            self.run = lambda self, *args, **kwargs: None

    def base_set_up(self, url, login_required=False, profile_required=False) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.profile = Profile(id=1,
                               user=self.user,
                               first_name='Test',
                               last_name='User',
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
