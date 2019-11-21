from django.urls import reverse

from seawatch_registration.models import Profile, Skill
from seawatch_registration.tests.views.test_base import TestBase


class TestAddSkillsView(TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('add_skills'), login_required=True, profile_required=True)

    def test_views__add_skills__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_skills__get__should_show_selected_skills_when_skills_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.skills.add(Skill.objects.filter(group='other').first())
        profile.skills.add(Skill.objects.filter(group='lang').first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_languages_')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_skills_')

    def test_views__add_skills__post__should_show_selected_skills_when_skills_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.skills.add(Skill.objects.filter(group='other').first())
        profile.skills.add(Skill.objects.filter(group='lang').first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_languages_')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_skills_')

    def test_views__add_skills__post__should_redirect_to_document_when_skills_are_set_to_zero(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.skills.add(skill)
        profile.skills.add(language)
        profile.save()

        # Act
        response = self.client.post(self.url,
                                    {},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, expected_url='/accounts/document/add/')
        self.assertEquals(len(profile.skills.all()), 0)

    def test_views__add_skills__post__should_redirect_to_document_when_skills_are_set_to_2(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.save()

        # Act
        response = self.client.post(self.url,
                                    {'skills': skill.id,
                                     'languages': language.id},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, expected_url='/accounts/document/add/')
        self.assertEquals(len(profile.skills.all()), 2)
