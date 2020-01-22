from datetime import date

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
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

        def base_set_up(self, url, login_required=False, profile_required=False, permission_required=False,
                        permission_name='', permission_class='') -> None:
            self.client = Client()
            self.username = 'testuser1'
            self.password = '1X<ISRUkw+tuK'
            self.user = User.objects.create_user(username=self.username,
                                                 password=self.password,
                                                 first_name='Test',
                                                 last_name='User',)

            if permission_required:
                content_type = ContentType.objects.get_for_model(permission_class)
                self.__permission = Permission.objects.get(
                    codename=permission_name,
                    content_type=content_type,
                )
                self.user.user_permissions.add(self.__permission)
            self.user.save()
            self.profile = Profile(id=1,
                                   user=self.user,
                                   citizenship=('DE', 'US'),
                                   date_of_birth=date.today(),
                                   place_of_birth='New York',
                                   country_of_birth='US',
                                   gender='m',
                                   needs_schengen_visa=False,
                                   phone='0123456789')
            self.profile.save()
            self.url = url
            self.__login_required = login_required
            self.__profile_required = profile_required
            self.__permission_required = permission_required

        def test__base__should_redirect_to_login_when_login_required_but_user_not_logged_in(self):
            if not self.__login_required:
                self.skipTest('login not required for ' + str(self.__class__))
            # Act
            response = self.client.get(self.url, user=self.user)

            # Assert
            self.assertRedirects(response, '/accounts/login/?next=' + self.url)

        def test__base__should_get_403_when_permission_required_but_user_dont_have_permission(self):
            if not self.__permission_required:
                self.skipTest('permission not required for ' + str(self.__class__))
            self.user.user_permissions.remove(self.__permission)
            # Act
            response = self.client.get(self.url, user=self.user)
            self.user.user_permissions.add(self.__permission)

            # Assert
            self.assertRedirects(response, '/accounts/login/?next=' + self.url)
