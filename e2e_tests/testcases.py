from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestCases:
    class SeleniumTestCase(LiveServerTestCase):

        def setUp(self) -> None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='e2e_tests/chromedriver')
            self.nav_item = None
            self.model_classes = list()
            self.nav_item_url = None

        def tearDown(self) -> None:
            self.browser.close()

        def assert_active_navbar(self):
            if self.nav_item is None:
                raise NotImplementedError
            navbar_link = self.browser.find_element_by_link_text(self.nav_item)
            self.assertTrue('active' in navbar_link.get_attribute('class'))

        def click_menu_item(self):
            self.browser.find_element_by_link_text(self.nav_item).click()

            self.assert_active_navbar()
            if self.nav_item_url is None:
                raise NotImplementedError
            self.assertEquals(self.browser.current_url, self.nav_item_url)

        def click_menu_item_from_index(self):
            self.browser.get(self.live_server_url)
            self.click_menu_item()

        def click_primary_button(self):
            self.browser.find_element_by_class_name('btn-primary').click()

        def count_table_rows(self):
            table_body = self.browser.find_element_by_tag_name('tbody')
            table_rows = table_body.find_elements_by_tag_name('tr')
            return len(table_rows)

    class SeleniumLoginTestCase(SeleniumTestCase):

        def setUp(self):
            super().setUp()
            self.username = 'TestUser'
            self.email = 'testmail@seawatch.org'
            self.first_name = 'Max'
            self.last_name = 'Mustermann'
            self.password = 'TopSecretPassword'
            self.login_url = self.live_server_url + reverse('login')

        def login(self):
            user = User.objects.create_user(username=self.username,
                                            password=self.password,
                                            email=self.email,
                                            first_name=self.first_name,
                                            last_name=self.last_name)
            if len(self.model_classes) > 0:
                permissions = list()
                for model_class in self.model_classes:
                    content_type = ContentType.objects.get_for_model(model_class)
                    permissions += list(Permission.objects.filter(content_type=content_type))
                user.user_permissions.set(permissions)

            self.browser.get(self.login_url)
            username_input = self.browser.find_element_by_name('username')
            username_input.send_keys(self.username)
            password_input = self.browser.find_element_by_name('password')
            password_input.send_keys(self.password)
            login_button = self.browser.find_element_by_class_name('btn-primary')

            self.assertEquals(login_button.text, 'Login')
            login_button.click()

