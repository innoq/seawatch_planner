from django.forms import Select
from django.urls import reverse

from e2e_tests.testcases import TestCases
from missions.models import Ship, DefaultAssignment
from seawatch_registration.models import Position


class TestDefaultAssignment(TestCases.SeleniumLoginTestCase):

    # noinspection PyAttributeOutsideInit
    def setUp(self) -> None:
        super().setUp()
        self.model_classes = [Ship, DefaultAssignment]
        self.nav_item = 'Ships'
        self.ship = ship = Ship(name='SeaWatch 3')
        ship.save()
        self.position = Position.objects.all().first()
        self.quantity = '2'

        self.nav_item_url = self.live_server_url + reverse('ship_list')

    def test_add_default_assigment(self):
        self.login()

        # ship list
        self.click_menu_item_from_index()

        # default assignment list of first ship
        self.browser.find_element_by_name('default_assignment').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.live_server_url + reverse('default_assignment_list',
                                                                                   kwargs={'ship_id': self.ship.id}))

        # add default assignment
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, reverse('default_assignment_add',
                                                            kwargs={'ship_id': self.ship.id}))
        Select(self.browser.find_element_by_name('position')).select_by_value(str(self.position.id))
        self.browser.find_element_by_name('quantity').send_keys(self.quantity)

        # default assignment list of first ship
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, reverse('default_assignment_list',
                                                            kwargs={'ship_id': self.ship.id}))
        self.assertEquals(self.count_table_rows(), 1)
        self.assertTrue(DefaultAssignment.objects.filter(ship=self.ship,
                                                         position=self.position,
                                                         quantity=self.quantity).exists())
