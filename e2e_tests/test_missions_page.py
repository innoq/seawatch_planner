from datetime import datetime

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.select import Select

from missions.models import Ship, Mission


class TestMissionsPage(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome('e2e_tests/chromedriver')
        self.username = 'TestUser'
        self.email = 'testmail@seawatch.org'
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.password = 'TopSecretPassword'
        self.name = 'Sabatical 2020'
        self.start_date = '01.01.2020'
        self.end_date = '23.12.2020'
        self.ship = Ship(name='SeaWatch 3')
        self.ship.save()

        self.login_url = self.live_server_url + reverse('login')
        self.mission_list_url = self.live_server_url + reverse('mission_list')
        self.mission_add_url = self.live_server_url + reverse('mission_create')

    def tearDown(self) -> None:
        self.browser.close()

    def test_add_mission(self):
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Missions').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)

        self.browser.find_element_by_class_name('btn-primary').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_add_url)
        self.browser.find_element_by_name('name').send_keys(self.name)
        self.browser.find_element_by_name('start_date').send_keys(self.start_date)
        self.browser.find_element_by_name('end_date').send_keys(self.end_date)
        ship_select = Select(self.browser.find_element_by_name('ship'))
        ship_select.select_by_value(str(self.ship.id))
        self.browser.find_element_by_class_name('btn-primary').click()

        self.browser.find_element_by_link_text('Missions').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)

        table_body = self.browser.find_element_by_tag_name('tbody')
        table_rows = table_body.find_elements_by_tag_name('tr')

        self.assert_active_navbar()
        self.assertEquals(len(table_rows), 1)

    def test_update_mission(self):
        mission = Mission(name=self.name,
                          start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                          end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                          ship=self.ship)
        mission.save()
        new_name = 'Weihnachts-Trip 2020'
        new_start_date = '24.12.2020'
        new_end_date = '26.12.2020'
        new_ship = Ship(name='SeaWatch 4')
        new_ship.save()
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Missions').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)
        self.browser.find_element_by_name('edit').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('mission_update', kwargs={'pk': mission.id}))

        name_input = self.browser.find_element_by_name('name')
        name_input.clear()
        name_input.send_keys(new_name)
        start_date_input = self.browser.find_element_by_name('start_date')
        start_date_input.clear()
        start_date_input.send_keys(new_start_date)
        end_date_input = self.browser.find_element_by_name('end_date')
        end_date_input.clear()
        end_date_input.send_keys(new_end_date)
        ship_select = Select(self.browser.find_element_by_name('ship'))
        ship_select.select_by_value(str(new_ship.id))
        self.browser.find_element_by_class_name('btn-primary').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)
        self.assertTrue(Mission.objects.filter(name=new_name,
                                               start_date=datetime.strptime(new_start_date, '%d.%m.%Y'),
                                               end_date=datetime.strptime(new_end_date, '%d.%m.%Y'),
                                               ship=new_ship).exists())

    def test_delete_mission(self):
        mission = Mission(name=self.name,
                          start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                          end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                          ship=self.ship)
        mission.save()
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Missions').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('mission_delete', kwargs={'pk': mission.id}))
        self.browser.find_element_by_class_name('btn-primary').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)
        self.assertEquals(len(Mission.objects.all()), 0)

    def test_cancel_question_deletion(self):
        mission = Mission(name=self.name,
                          start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                          end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                          ship=self.ship)
        mission.save()
        self.login()
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_link_text('Missions').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('mission_delete', kwargs={'pk': mission.id}))
        self.browser.find_element_by_link_text('Cancel').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.mission_list_url)
        self.assertTrue(Mission.objects.filter(name=self.name,
                                               start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                                               end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                                               ship=self.ship).exists())

    def login(self):
        user = User.objects.create_user(username=self.username,
                                        password=self.password,
                                        email=self.email,
                                        first_name=self.first_name,
                                        last_name=self.last_name)
        content_type = ContentType.objects.get_for_model(Mission)
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
        navbar_link = self.browser.find_element_by_link_text('Missions')
        self.assertTrue('active' in navbar_link.get_attribute('class'))
