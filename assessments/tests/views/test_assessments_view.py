from django.urls import reverse

from assessments.models import Assessment
from assessments.tests.test_base import TestBases
from seawatch_registration.models import Position


class TestShowAssessmentsView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('assessments'), login_required=True, permission_required=True,
                         permission_name='can_assess_profiles', permission_class=Assessment)

    def test_views__show_assessments__get__should_show_text_when_no_pending_assessments_are_avaiable(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessments.html')
        self.assertContains(response, 'There are no pending assessments!')

    def test_views__show_assessments__get__should_show_text_when__assessment_is_status_rejected(self):
        # Arrange
        profile = self.profile
        position = Position.objects.all().first()
        profile.save()
        profile.requested_positions.set((position,))
        assessment = Assessment(profile=self.profile, status='rejected')
        assessment.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessments.html')
        self.assertContains(response, 'There are no pending assessments!')

    def test_views__show_assessments__get__should_show_text_when__assessment_is_status_approved(self):
        # Arrange
        profile = self.profile
        position = Position.objects.all().first()
        profile.save()
        profile.requested_positions.set((position,))
        assessment = Assessment(profile=self.profile, status='approved')
        assessment.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessments.html')
        self.assertContains(response, 'There are no pending assessments!')

    def test_views__show_assessments__get__should_show_table_when_pending_assessment_is_available(self):
        # Arrange
        profile = self.profile
        position = Position.objects.all().first()
        profile.save()
        profile.requested_positions.set((position,))
        assessment = Assessment(profile=self.profile, status='pending')
        assessment.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assessments.html')
        self.assertContains(response, self.td(profile.first_name))
        self.assertContains(response, self.td(profile.last_name))
        self.assertContains(response, self.td(profile.pk))
        self.assertContains(response, position)
        self.assertContains(response, self.tr_onclick(profile.pk))

    @staticmethod
    def td(value):
        return '<td>' + str(value) + '</td>'

    @staticmethod
    def tr_onclick(primary_key):
        return '<tr onclick="window.location=\'' + str(primary_key) + '/\';">'
