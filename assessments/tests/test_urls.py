from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

import assessments.views.assessment as assessment


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_assessment_list(self):
        url = reverse('assessment_list')
        self.assertEquals(resolve(url).func.__name__, assessment.ListView.as_view().__name__)

    def test_urls_assessment(self):
        url = reverse('assessment_update', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.__name__, assessment.UpdateView.as_view().__name__)
