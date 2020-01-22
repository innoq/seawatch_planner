from django.test import Client, SimpleTestCase
from django.urls import resolve, reverse

import seawatch_registration.views.availability as availability
import seawatch_registration.views.document as document
import seawatch_registration.views.position as position
import seawatch_registration.views.profile as profile
import seawatch_registration.views.question as question
import seawatch_registration.views.skill as skill
from seawatch_registration.views.signup import SignupView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_profile_detail(self):
        url = reverse('profile_detail')
        self.assertEquals(resolve(url).func.__name__, profile.DetailView.as_view().__name__)

    def test_urls_profile_create(self):
        url = reverse('profile_create')
        self.assertEquals(resolve(url).func.__name__, profile.ProfileCreateView.as_view().__name__)

    def test_urls_profile_update(self):
        url = reverse('profile_update')
        self.assertEquals(resolve(url).func.__name__, profile.UpdateView.as_view().__name__)

    def test_urls_signup(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.__name__, SignupView.as_view().__name__)

    def test_urls_document_create(self):
        url = reverse('document_create')
        self.assertEquals(resolve(url).func.__name__, document.DocumentCreateView.as_view().__name__)

    def test_urls_add_requested_positions(self):
        url = reverse('requested_position_update')
        self.assertEquals(resolve(url).func.__name__, position.PositionUpdateView.as_view().__name__)

    def test_urls_skill_update(self):
        url = reverse('skill_update')
        self.assertEquals(resolve(url).func.__name__, skill.SkillsUpdateView.as_view().__name__)

    def test_urls_question_answer(self):
        url = reverse('question_answer')
        self.assertEquals(resolve(url).func.__name__, question.AnsweringQuestionsView.as_view().__name__)

    def test_urls_availabilities(self):
        url = reverse('availability_list')
        self.assertEquals(resolve(url).func.__name__, availability.AvailabilityListView.as_view().__name__)

    def test_urls_availabilities_create(self):
        url = reverse('availability_create')
        self.assertEquals(resolve(url).func.__name__, availability.CreateView.as_view().__name__)
