from django.contrib.auth.models import User
from django.urls import reverse

from e2e_tests.testcases import TestCases


class TestSignup(TestCases.SeleniumTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'

        self.nav_item = 'Signup'
        self.nav_item_url = self.live_server_url + reverse('signup')
        self.create_profile_url = self.live_server_url + reverse('profile_create')

    def test_user_can_sign_up(self):
        self.click_menu_item_from_index()
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys(self.email)
        first_name_input = self.browser.find_element_by_name('first_name')
        first_name_input.send_keys(self.first_name)
        last_name_input = self.browser.find_element_by_name('last_name')
        last_name_input.send_keys(self.last_name)
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys(self.password)
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys(self.password)
        self.click_primary_button()

        self.assertEquals(self.browser.current_url, self.create_profile_url + '?initial_registration=yes')
        self.assertTrue(User.objects.filter(email=self.email).exists())
        self.assertTrue(User.objects.filter(username=self.email).exists())
