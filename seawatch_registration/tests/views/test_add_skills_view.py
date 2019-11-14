from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from seawatch_registration.models import Profile, Skill
from seawatch_registration.tests.views import util


class TestAddSkillsView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.url_add_skills = reverse('add_skills')

    def test_views__add_skills__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/skills/')

    def test_views__add_skills__get__should_get_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__add_skills__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_skills__get__should_show_selected_skills_when_skills_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.skills.add(Skill.objects.filter(group='other').first())
        profile.skills.add(Skill.objects.filter(group='lang').first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_languages_')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_skills_')

    def test_views__add_skills__post__should_show_selected_skills_when_skills_exists(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.skills.add(Skill.objects.filter(group='other').first())
        profile.skills.add(Skill.objects.filter(group='lang').first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_languages_')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_skills_')

    def test_views__add_skills__post__should_render_success_when_skills_are_set_to_zero(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.skills.add(skill)
        profile.skills.add(language)
        profile.save()

        # Act
        response = self.client.post(self.url_add_skills,
                                    {},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(len(profile.skills.all()), 0)

    def test_views__add_skills__post__should_render_success_when_skills_are_set_to_2(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
        skill = Skill.objects.filter(group='other').first()
        language = Skill.objects.filter(group='lang').first()
        profile.save()

        # Act
        response = self.client.post(self.url_add_skills,
                                    {'skills': skill.id,
                                     'languages': language.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(len(profile.skills.all()), 2)
