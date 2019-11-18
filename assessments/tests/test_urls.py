from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from assessments.views.assessment_view import AssessmentView
from assessments.views.assessments_view import AssessmentOverviewView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_assessment_overview(self):
        url = reverse('assessments')
        self.assertEquals(resolve(url).func.__name__, AssessmentOverviewView.as_view().__name__)

    def test_urls_assessment(self):
        url = reverse('assessment', kwargs={'profile_id': 1})
        self.assertEquals(resolve(url).func.__name__, AssessmentView.as_view().__name__)
