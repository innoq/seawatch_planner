from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from missions.models import Ship


class TestShipPage(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('e2e_tests/chromedriver')
        self.username = 'TestUser'
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'
        self.name = 'SeaWatch 3'

        self.login_url = self.live_server_url + reverse('login')
        self.ship_list_url = self.live_server_url + reverse('ship_list')
        self.ship_add_url = self.live_server_url + reverse('ship_create')

    def tearDown(self) -> None:
        self.browser.close()

    def test_add_ship(self):
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Ships').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)

        self.browser.find_element_by_class_name('btn-primary').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_add_url)
        self.browser.find_element_by_name('name').send_keys(self.name)
        self.browser.find_element_by_class_name('btn-primary').click()
        table_body = self.browser.find_element_by_tag_name('tbody')
        table_rows = table_body.find_elements_by_tag_name('tr')

        self.assert_active_navbar()
        self.assertEquals(len(table_rows), 1)
        self.assertTrue(Ship.objects.filter(name=self.name).exists())

    def test_update_ship(self):
        ship = Ship(name=self.name)
        ship.save()
        new_name = 'SeaWatch 4'
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Ships').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)
        self.browser.find_element_by_name('edit').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_update', kwargs={'pk': ship.id}))

        text_input = self.browser.find_element_by_name('name')
        text_input.clear()
        text_input.send_keys(new_name)
        self.browser.find_element_by_class_name('btn-primary').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)
        self.assertTrue(Ship.objects.filter(name=new_name).exists())

    def test_delete_ship(self):
        ship = Ship(name=self.name)
        ship.save()
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Ships').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_delete', kwargs={'pk': ship.id}))
        self.browser.find_element_by_class_name('btn-primary').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)
        self.assertEquals(len(Ship.objects.all()), 0)

    def test_cancel_question_deletion(self):
        ship = Ship(name=self.name)
        ship.save()
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Ships').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_delete', kwargs={'pk': ship.id}))
        self.browser.find_element_by_link_text('Cancel').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.ship_list_url)
        self.assertTrue(Ship.objects.filter(name=self.name).exists())

    def login(self):
        user = User.objects.create_user(username=self.username,
                                        password=self.password,
                                        email=self.email,
                                        first_name=self.first_name,
                                        last_name=self.last_name)
        content_type = ContentType.objects.get_for_model(Ship)
        permissions = list(Permission.objects.filter(content_type=content_type))
        user.user_permissions.set(permissions)

        self.browser.get(self.login_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        login_button = self.browser.find_element_by_class_name('btn-primary')

        self.assertEquals(login_button.text, 'Login')
        login_button.click()

    def assert_active_navbar(self):
        navbar_link = self.browser.find_element_by_link_text('Ships')
        self.assertTrue('active' in navbar_link.get_attribute('class'))
