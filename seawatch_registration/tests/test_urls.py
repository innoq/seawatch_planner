from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from seawatch_registration.views.document_create_view import DocumentCreateView
from seawatch_registration.views.profile_create_view import ProfileCreateView
from seawatch_registration.views.profile_detail_view import ProfileDetailView
from seawatch_registration.views.profile_update_view import ProfileUpdateView
from seawatch_registration.views.question_update_view import QuestionUpdateView
from seawatch_registration.views.requested_position_update_view import RequestedPositionUpdateView
from seawatch_registration.views.signup_view import SignupView
from seawatch_registration.views.skill_update_view import SkillUpdateView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_profile_detail(self):
        url = reverse('profile_detail')
        self.assertEquals(resolve(url).func.__name__, ProfileDetailView.as_view().__name__)

    def test_urls_profile_create(self):
        url = reverse('profile_create')
        self.assertEquals(resolve(url).func.__name__, ProfileCreateView.as_view().__name__)

    def test_urls_profile_update(self):
        url = reverse('profile_update')
        self.assertEquals(resolve(url).func.__name__, ProfileUpdateView.as_view().__name__)

    def test_urls_signup(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.__name__, SignupView.as_view().__name__)

    def test_urls_document_create(self):
        url = reverse('document_create')
        self.assertEquals(resolve(url).func.__name__, DocumentCreateView.as_view().__name__)

    def test_urls_add_requested_positions(self):
        url = reverse('requested_position_update')
        self.assertEquals(resolve(url).func.__name__, RequestedPositionUpdateView.as_view().__name__)

    def test_urls_skill_update(self):
        url = reverse('skill_update')
        self.assertEquals(resolve(url).func.__name__, SkillUpdateView.as_view().__name__)

    def test_urls_question_update(self):
        url = reverse('question_update')
        self.assertEquals(resolve(url).func.__name__, QuestionUpdateView.as_view().__name__)
