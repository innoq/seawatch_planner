from datetime import datetime

from django.urls import reverse
from selenium.webdriver.support.select import Select

from e2e_tests.testcases import TestCases
from missions.models import Ship, Mission


class TestMission(TestCases.SeleniumLoginTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.nav_item = 'Missions'
        self.model_classes = [Mission]

        self.name = 'Sabatical 2020'
        self.start_date = '01.01.2020'
        self.end_date = '23.12.2020'
        self.ship = Ship(name='SeaWatch 3')
        self.ship.save()

        self.login_url = self.live_server_url + reverse('login')
        self.nav_item_url = self.live_server_url + reverse('mission_list')
        self.add_url = self.live_server_url + reverse('mission_create')

    def test_add_mission(self):
        self.login()
        self.click_menu_item_from_index()
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.add_url)

        self.browser.find_element_by_name('name').send_keys(self.name)
        self.browser.find_element_by_name('start_date').send_keys(self.start_date)
        self.browser.find_element_by_name('end_date').send_keys(self.end_date)
        ship_select = Select(self.browser.find_element_by_name('ship'))
        ship_select.select_by_value(str(self.ship.id))
        self.click_primary_button()

        self.click_menu_item()

        self.assert_active_navbar()
        self.assertEquals(self.count_table_rows(), 1)

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
        self.click_menu_item_from_index()
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
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
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
        self.click_menu_item_from_index()

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('mission_delete', kwargs={'pk': mission.id}))
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertEquals(len(Mission.objects.all()), 0)

    def test_cancel_question_deletion(self):
        mission = Mission(name=self.name,
                          start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                          end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                          ship=self.ship)
        mission.save()
        self.login()
        self.click_menu_item_from_index()

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('mission_delete', kwargs={'pk': mission.id}))
        self.browser.find_element_by_link_text('Cancel').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertTrue(Mission.objects.filter(name=self.name,
                                               start_date=datetime.strptime(self.start_date, '%d.%m.%Y'),
                                               end_date=datetime.strptime(self.end_date, '%d.%m.%Y'),
                                               ship=self.ship).exists())
