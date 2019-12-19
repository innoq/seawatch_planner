from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver


class TestSignupPage(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('e2e_tests/chromedriver')
        self.username = 'TestUser'
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'

        self.signup_url = self.live_server_url + reverse('signup')

    def tearDown(self) -> None:
        self.browser.close()

    def test_get_to_sign_up_page_from_index(self):
        self.browser.get(self.live_server_url)
        signup_link = self.browser.find_element_by_link_text('Signup')

        self.assertIsNotNone(signup_link)
        signup_link.click()
        self.assertEquals(
            self.browser.current_url,
            self.signup_url
        )

    def test_user_can_sign_up(self):
        self.browser.get(self.signup_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
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
        signup_button = self.browser.find_element_by_class_name('btn-primary')

        self.assertEquals(signup_button.text, 'Sign up')
        signup_button.click()

        self.assertEquals(self.browser.current_url, self.live_server_url + reverse('profile_create'))
        self.assertTrue(User.objects.filter(username=self.username).exists())