from django.contrib.auth.models import User
from django.urls import reverse

from assessments.models import Assessment
from e2e_tests.testcases import TestCases
from missions.models import Ship, Assignment, Mission
from seawatch_registration.models import Position, Profile, Availability


class TestAssigneeView(TestCases.SeleniumLoginTestCase):

    # noinspection PyAttributeOutsideInit
    def setUp(self) -> None:
        super().setUp()
        self.model_classes = [Mission, Assignment, Assessment, Profile, Position]
        self.nav_item = 'Missions'
        self.ship = Ship.objects.create(name='SeaWatch 3')
        self.position = Position.objects.create(name='Beelzebub')
        self.mission = Mission.objects.create(
            name='Spring cleaning in hell',
            ship=self.ship,
            start_date='2012-11-21',
            end_date='2012-12-21')
        self.nav_item_url = self.live_server_url + reverse('mission_list')

    def test__assignment_create__can_create_an_assignment_for_mission(self):
        self._local_setup()

        # prepare: navigate to mission
        self._navigate_to_mission_detail_view()

        # act: create a new assignment
        self.click_primary_button()
        self._assert_current_path_is_assignment_create()
        self.browser.find_element_by_id('id_position').send_keys(self.position.name)
        self.click_primary_button()

        # assert: assignment was created
        self._assert_current_path_is_mission_detail()
        self.assertEqual(1, len(self.browser.find_elements_by_xpath('//table/tbody/tr')))

    def test__assign_view__click_on_assignment_only_displays_matches_for_current_mission(self):
        self._local_setup()

        # prepare: create profiles
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)

        candidate_match = self._get_candidate(username='kain@baal.com')
        candidate_match.profile.approved_positions.add(self.position)
        Availability.objects.create(profile=candidate_match.profile, start_date='2012-10-01', end_date='2012-12-30')

        candidate_mismatch = self._get_candidate(username='abel@baal.com')
        candidate_mismatch.profile.approved_positions.add(Position.objects.create(name='Janitor'))

        # prepare: navigate to assignee view
        self._navigate_to_assignee_view_from_mission_detail_view(assignment)

        # assert: correct candidate matches
        self.assertEqual(1, len(self.browser.find_elements_by_xpath('//table/tbody/tr')))
        self.assertEqual(candidate_match.first_name + ' ' + candidate_match.last_name,
                         self.browser.find_element_by_xpath('//table/tbody/tr/td[2]').text)

    def test__assign_view__the_current_assignee_is_always_displayed(self):
        self._local_setup()

        # prepare: create an assignment with assignee
        # who does not match since they have no availabilities or positions
        assignment = Assignment.objects.create(
            user=self._get_candidate(username='kain@baal.com'),
            mission=self.mission,
            position=self.position)

        # prepare: navigate to assignee view
        self._navigate_to_assignee_view_from_mission_detail_view(assignment)

        # assert: that one user is present and selected
        self.assertEqual(1, len(self.browser.find_elements_by_xpath('//table/tbody/tr')))
        self.assertEqual(1, len(self.browser.find_elements_by_xpath('//table//input[@checked]')))

    def test__assign_view__no_parameters_will_display_all_users(self):
        self._local_setup()

        # prepare: create some candidates
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)
        for name in ('fee', 'fi', 'fo', 'fam'):
            self._get_candidate(username=name + '@bigfoot.com')

        # prepare: navigate to assignee view
        self.browser.get(self.live_server_url + reverse('assignee', kwargs={'mission__id': self.mission.pk,
                                                                            'assignment__id': assignment.pk}))

        # assert: that all four users are present and nobody is selected
        self.assertEqual(4, len(self.browser.find_elements_by_xpath('//table/tbody/tr')))
        self.assertEqual(0, len(self.browser.find_elements_by_xpath('//table//input[@checked]')))

    def test__assign_view__can_filter_by_name_case_insensitive(self):
        self._local_setup()

        # prepare: create some candidates
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)
        for name in ('fee', 'fi', 'fo', 'fam'):
            self._get_candidate(username=name + '@bigfoot.com')

        # prepare: navigate to assignee view
        self.browser.get((self.live_server_url +
                          reverse('assignee', kwargs={'mission__id': self.mission.pk,
                                                      'assignment__id': assignment.pk}) +
                          '?name=eE'))

        # assert: that only 'fee' is displayed
        self.assertEqual(1, len(self.browser.find_elements_by_xpath('//table/tbody/tr')))
        self.assertEqual('fee@bigfoot.com last', self.browser.find_element_by_xpath('//table/tbody/tr/td[2]').text)

    def test__assign_view__filters_are_hidden_by_default(self):
        self._local_setup()

        # prepare: navigate to assignee view
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)
        self._navigate_to_assignee_view_directly(assignment)

        # assert
        self.assertEqual(0, len(self.browser.find_elements_by_class_name('show')))

    def test__assign_view__filters_are_shown_when_parameter_is_set(self):
        self._local_setup()

        # prepare: navigate to assignee view
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)
        self.browser.get((self.live_server_url +
                          reverse('assignee', kwargs={'mission__id': self.mission.pk,
                                                      'assignment__id': assignment.pk}) +
                          '?show_filter=true'))

        # assert
        self.assertEqual(1, len(self.browser.find_elements_by_class_name('show')))

    def test__assign_view__clicking_show_filter_will_append_get_url_parameter(self):
        self._local_setup()

        # prepare: navigate to assignee view
        assignment = Assignment.objects.create(mission=self.mission, position=self.position)
        self._navigate_to_assignee_view_directly(assignment)
        self.assertFalse('show_filter=true' in self.browser.current_url)
        self.browser.find_element_by_id('collapse-button').click()

        # assert
        self.assertTrue('show_filter=true' in self.browser.current_url)

    @staticmethod
    def _get_candidate(username):
        candidate = User.objects.create(
            first_name=username,
            last_name='last',
            username=username)
        Profile.objects.create(
            user=candidate,
            date_of_birth='2000-01-01',
            needs_schengen_visa=False,
            gender='d', country_of_birth='US', place_of_birth='Minneapolis', phone=0)
        return candidate

    def _local_setup(self):
        self.login()
        self.click_menu_item_from_index()
        self.assert_active_navbar()

    def _navigate_to_assignee_view_from_mission_detail_view(self, assignment):
        self._navigate_to_mission_detail_view()
        self.browser.find_element_by_id('assignee').click()
        self.assertEqual(
            reverse('assignee', kwargs={'mission__id': self.mission.pk, 'assignment__id': assignment.pk}),
            self.get_current_path_without_parameters())

    def _navigate_to_mission_detail_view(self):
        self.browser.find_element_by_id('assign_volunteer').click()
        self._assert_current_path_is_mission_detail()

    def _navigate_to_assignee_view_directly(self, assignment):
        self.browser.get((self.live_server_url +
                          reverse('assignee', kwargs={'mission__id': self.mission.pk,
                                                      'assignment__id': assignment.pk})))

    def _assert_current_path_is_mission_detail(self):
        self.assertEqual(
            reverse('mission_detail', kwargs={'pk': self.mission.pk}),
            self.get_current_path())

    def _assert_current_path_is_assignment_create(self):
        self.assertEqual(
            reverse('assignment_create', kwargs={'mission__id': self.mission.pk}),
            self.get_current_path())
