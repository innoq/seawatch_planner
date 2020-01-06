from django.contrib.auth.models import User
from django.urls import reverse

from e2e_tests.testcases import TestCases


class TestLogin(TestCases.SeleniumTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.nav_item = 'Login'

        self.username = 'TestUser'
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'

        self.nav_item_url = self.live_server_url + reverse('login')
        self.registration_process_url = self.live_server_url + reverse('registration_process')

    def test_user_can_login(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.click_menu_item_from_index()
        self.assert_active_navbar()

        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        self.click_primary_button()

        self.assertEquals(self.browser.current_url, self.registration_process_url)
        logout_link = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_link)

    def test_user_can_not_login_adn_gets_alert_if_password_is_wrong(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.click_menu_item_from_index()
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('WrongPassword')
        self.click_primary_button()

        self.assertEquals(self.browser.current_url, self.nav_item_url)
        alert = self.browser.find_element_by_class_name('alert')
        self.assertIsNotNone(alert)

    def test_user_can_not_login_adn_gets_alert_if_username_is_wrong(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.click_menu_item_from_index()
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('WrongUsername')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        self.click_primary_button()

        self.assertEquals(self.browser.current_url, self.nav_item_url)
        alert = self.browser.find_element_by_class_name('alert')
        self.assertIsNotNone(alert)
