from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse

from seawatch_registration.views import show_profile, add_profile, edit_profile, signup, add_document, AddSkillsView


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_urls_show_profile(self):
        url = reverse('show_profile')
        self.assertEquals(resolve(url).func, show_profile)

    def test_urls_add_profile(self):
        url = reverse('add_profile')
        self.assertEquals(resolve(url).func, add_profile)

    def test_urls_edit_profile(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)

    def test_urls_signup(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    def test_urls_add_document(self):
        url = reverse('add_document')
        self.assertEquals(resolve(url).func, add_document)

    def test_urls_add_skills(self):
        url = reverse('add_skills')
        self.assertEquals(resolve(url).func.__name__, AddSkillsView.as_view().__name__)
