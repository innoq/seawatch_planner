from django.urls import reverse

from e2e_tests.testcases import TestCases
from missions.models import Ship


class TestShip(TestCases.SeleniumLoginTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.model_classes = [Ship]
        self.nav_item = 'Ships'
        self.name = 'SeaWatch 3'

        self.login_url = self.live_server_url + reverse('login')
        self.nav_item_url = self.live_server_url + reverse('ship_list')
        self.add_url = self.live_server_url + reverse('ship_create')

    def test_add_ship(self):
        self.login()
        self.click_menu_item_from_index()
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.add_url)

        self.browser.find_element_by_name('name').send_keys(self.name)
        self.browser.find_element_by_class_name('btn-primary').click()

        self.assert_active_navbar()
        self.assertEquals(self.count_table_rows(), 1)
        self.assertTrue(Ship.objects.filter(name=self.name).exists())

    def test_update_ship(self):
        ship = Ship(name=self.name)
        ship.save()
        new_name = 'SeaWatch 4'
        self.login()
        self.click_menu_item_from_index()
        self.browser.find_element_by_name('edit').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_update', kwargs={'pk': ship.id}))

        text_input = self.browser.find_element_by_name('name')
        text_input.clear()
        text_input.send_keys(new_name)
        self.click_primary_button()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertTrue(Ship.objects.filter(name=new_name).exists())

    def test_delete_ship(self):
        ship = Ship(name=self.name)
        ship.save()
        self.login()
        self.click_menu_item_from_index()

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_delete', kwargs={'pk': ship.id}))
        self.click_primary_button()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertEquals(len(Ship.objects.all()), 0)

    def test_cancel_question_deletion(self):
        ship = Ship(name=self.name)
        ship.save()
        self.login()
        self.click_menu_item_from_index()

        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('ship_delete', kwargs={'pk': ship.id}))
        self.browser.find_element_by_link_text('Cancel').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertTrue(Ship.objects.filter(name=self.name).exists())
