from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from seawatch_registration.views.add_document_view import AddDocumentView
from seawatch_registration.views.add_profile_view import AddProfileView
from seawatch_registration.views.add_skills_view import AddSkillsView
from seawatch_registration.views.assessment_view import AssessmentView
from seawatch_registration.views.edit_profile_view import EditProfileView
from seawatch_registration.views.questions_view import QuestionView
from seawatch_registration.views.requested_positions_view import RequestedPositionView
from seawatch_registration.views.assessments_view import AssessmentOverviewView

from seawatch_registration.views.show_profile_view import ShowProfileView
from seawatch_registration.views.signup_view import SignupView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_show_profile(self):
        url = reverse('show_profile')
        self.assertEquals(resolve(url).func.__name__, ShowProfileView.as_view().__name__)

    def test_urls_add_profile(self):
        url = reverse('add_profile')
        self.assertEquals(resolve(url).func.__name__, AddProfileView.as_view().__name__)

    def test_urls_edit_profile(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func.__name__, EditProfileView.as_view().__name__)

    def test_urls_signup(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.__name__, SignupView.as_view().__name__)

    def test_urls_add_document(self):
        url = reverse('add_document')
        self.assertEquals(resolve(url).func.__name__, AddDocumentView.as_view().__name__)

    def test_urls_add_requested_positions(self):
        url = reverse('add_requested_profile')
        self.assertEquals(resolve(url).func.__name__, RequestedPositionView.as_view().__name__)

    def test_urls_add_skills(self):
        url = reverse('add_skills')
        self.assertEquals(resolve(url).func.__name__, AddSkillsView.as_view().__name__)

    def test_urls_questions(self):
        url = reverse('questions')
        self.assertEquals(resolve(url).func.__name__, QuestionView.as_view().__name__)

    def test_urls_assessment_overview(self):
        url = reverse('assessments')
        self.assertEquals(resolve(url).func.__name__, AssessmentOverviewView.as_view().__name__)

    def test_urls_assessment(self):
        url = reverse('assessment', kwargs={'profile_id': 1})
        self.assertEquals(resolve(url).func.__name__, AssessmentView.as_view().__name__)
