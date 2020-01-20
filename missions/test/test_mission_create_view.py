from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from missions.models import Mission, Ship, DefaultAssignment
from seawatch_registration.models import Position


class TestMissionCreateView(TestCase):

    def setUp(self) -> None:
        client = Client()
        admin = User.objects.create_user(
            username='admin',
            password='12345')
        admin.is_superuser = True
        admin.save()
        client.force_login(admin)

        self.client = client
        self.ship = Ship.objects.create(name='SeaWatch 4')
        self.position = Position.objects.create(name='Master')

    def test_ship_can_have_no_default_assignments(self):
        # given the ship has no default assignments
        # when
        self.client.post(reverse('mission_create'), data={
            **self._get_example_mission_data(),
            'create_default_assignments': True
        })

        # then
        self.assertEqual(1, Mission.objects.count())
        self.assertEqual(0, Mission.objects.first().assignment_set.count())

    def test_default_assignments_are_created(self):
        # given
        DefaultAssignment.objects.create(
            ship=self.ship, position=self.position, quantity=3)

        # when
        self.client.post(reverse('mission_create'), data={
            **self._get_example_mission_data(),
            'create_default_assignments': True
        })

        # then
        self.assertEqual(1, Mission.objects.count())
        self.assertEqual(3, Mission.objects.first().assignment_set.count())

    def test_default_assignments_are_not_created(self):
        # given
        DefaultAssignment.objects.create(ship=self.ship, position=self.position, quantity=3)

        # when
        self.client.post(reverse('mission_create'), data={
            **self._get_example_mission_data(),
            'create_default_assignments': False
        })

        # then
        self.assertEqual(1, Mission.objects.count())
        self.assertEqual(0, Mission.objects.first().assignment_set.count())

    def _get_example_mission_data(self):
        return {
            'name': 'Super mission',
            'start_date': '12/12/2019',
            'end_date': '12/12/2020',
            'ship': self.ship.pk,
        }
