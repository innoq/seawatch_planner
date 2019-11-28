from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from assessments.views.assessment_list_view import AssessmentListView
from assessments.views.assessment_view import AssessmentUpdateView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_assessment_list(self):
        url = reverse('assessment_list')
        self.assertEquals(resolve(url).func.__name__, AssessmentListView.as_view().__name__)

    def test_urls_assessment(self):
        url = reverse('assessment', kwargs={'profile_id': 1})
        self.assertEquals(resolve(url).func.__name__, AssessmentUpdateView.as_view().__name__)
