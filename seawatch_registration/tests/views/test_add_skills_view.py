from django.urls import reverse

from seawatch_registration.models import Profile, Skill
from seawatch_registration.tests.views.test_base import TestBases


class TestAddSkillsView(TestBases.TestBase):

    def setUp(self) -> None:
        self.base_set_up(url=reverse('skill_update'), login_required=True, profile_required=True)

    def test_views__skill_update__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.profile
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__skill_update__get__should_show_selected_skills_when_skills_exists(self):
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

    def test_views__skill_update__post__should_show_selected_skills_when_skills_exists(self):
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

    def test_views__skill_update__post__should_redirect_to_document_when_skills_are_set_to_zero(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.skills.add(skill)
        profile.skills.add(language)
        profile.save()

        # Act
        response = self.client.post(self.url + '?initial_registration',
                                    {'languages': language.id},
                                    user=self.user)

        # Assert
        self.assertEquals(len(profile.skills.all()), 1)
        self.assertRedirects(response, expected_url='/accounts/documents/add/?initial_registration=yes')

    def test_views__skill_update__post__should_redirect_to_document_when_skills_are_set_to_2(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.profile
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.save()

        # Act
        response = self.client.post(self.url + '?initial_registration',
                                    {'skills': skill.id,
                                     'languages': language.id},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, expected_url='/accounts/documents/add/?initial_registration=yes')
        self.assertEquals(len(profile.skills.all()), 2)
