from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver


class TestLoginPage(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('e2e_tests/chromedriver')
        self.username = 'TestUser'
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'

        self.login_url = self.live_server_url + reverse('login')

    def tearDown(self) -> None:
        self.browser.close()

    def test_get_to_login_page_from_index(self):
        self.browser.get(self.live_server_url)
        login_link = self.browser.find_element_by_link_text('Login')

        self.assertIsNotNone(login_link)
        login_link.click()
        self.assertEquals(
            self.browser.current_url,
            self.login_url
        )

    def test_user_can_login(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.browser.get(self.login_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        login_button = self.browser.find_element_by_class_name('btn-primary')

        self.assertEquals(login_button.text, 'Login')
        login_button.click()

        self.assertEquals(self.browser.current_url, self.live_server_url + reverse('registration_process'))
        logout_link = self.browser.find_element_by_link_text('Logout')
        self.assertIsNotNone(logout_link)

    def test_user_can_not_login_adn_gets_alert_if_password_is_wrong(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.browser.get(self.login_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys('WrongPassword')
        login_button = self.browser.find_element_by_class_name('btn-primary')

        self.assertEquals(login_button.text, 'Login')
        login_button.click()

        self.assertEquals(self.browser.current_url, self.login_url)
        alert = self.browser.find_element_by_class_name('alert')
        self.assertIsNotNone(alert)

    def test_user_can_not_login_adn_gets_alert_if_username_is_wrong(self):
        User.objects.create_user(username=self.username,
                                 password=self.password,
                                 email=self.email,
                                 first_name=self.first_name,
                                 last_name=self.last_name)

        self.browser.get(self.login_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('WorngUsername')
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        login_button = self.browser.find_element_by_class_name('btn-primary')

        self.assertEquals(login_button.text, 'Login')
        login_button.click()

        self.assertEquals(self.browser.current_url, self.login_url)
        alert = self.browser.find_element_by_class_name('alert')
        self.assertIsNotNone(alert)
