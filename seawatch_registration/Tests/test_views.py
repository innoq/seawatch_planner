import datetime
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from seawatch_registration.models import Profile, DocumentType, Document, Skill, Position, Question, Answer


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.user.save()
        self.url_add_profile = reverse('add_profile')
        self.url_edit_profile = reverse('edit_profile')
        self.url_show_profile = reverse('show_profile')
        self.url_add_document = reverse('add_document')
        self.url_add_skills = reverse('add_skills')
        self.url_add_positions = reverse('add_requested_profile')
        self.url_questions = reverse('questions')

    def test_views__add_profile__get__should_redirect_to_login_when_user_is_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_profile, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/add/')

    def test_views__add_profile__get__should_return_profile_form(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_profile, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_views__add_profile__post__should_redirect_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_add_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch',
                                     'date_of_birth': datetime.date.today(),
                                     'place_of_birth': 'New York',
                                     'country_of_birth': 'United States of America',
                                     'gender': 'm',
                                     'needs_schengen_visa': False,
                                     'phone': '0123456789'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Profile.objects.all().count(), 1)

    def test_views__add_profile__post__should_not_redirect_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_add_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEquals(Profile.objects.all().count(), 0)

    def test_views__edit_profile__get__should_redirect_when_no_profile_exists(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_edit_profile)

        # Assert
        self.assertRedirects(response, self.url_add_profile)

    def test_views__edit_profile__get__should_get_profile_form_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_edit_profile)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_views__edit_profile__post__should_edit_profile_when_profile_for_user_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_edit_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch',
                                     'date_of_birth': datetime.date.today(),
                                     'place_of_birth': 'New York',
                                     'country_of_birth': 'United States of America',
                                     'gender': 'm',
                                     'needs_schengen_visa': False,
                                     'phone': '0987654321'},
                                    user=self.user)

        # Assert
        self.assertRedirects(response, self.url_show_profile)
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0987654321')

    def test_views__edit_profile__post__should_not_edit_profile_when_required_data_is_missing(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_edit_profile,
                                    {'user': self.user.id,
                                     'first_name': 'Test',
                                     'last_name': 'User',
                                     'citizenship': 'Deutsch'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().phone, '0123456789')

    def test_views__show_profile__get__should_render_with_show_profile_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'show-profile.html')

    def test_views__show_profile__get__should_redirect_to_login_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertRedirects(response, self.url_add_profile)

    def test_views__show_profile__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_show_profile, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/show/')

    def test_views__add_document__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/document/add/')

    def test_views__add_document__get__should_redirect_to_login_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertRedirects(response, self.url_add_profile)

    def test_views__add_document__get__should_render_with_document_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_document, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document.html')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_views__add_document__post__should_render_success_when_form_is_valid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.get_profile()
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()
        image = SimpleUploadedFile("testfile.jpg", b"file_content", content_type="image/jpg")

        # Act
        response = self.client.post(self.url_add_document,
                                    {'document_type': document_type.id,
                                     'number': '1234',
                                     'issuing_date': datetime.date.today(),
                                     'expiry_date': datetime.date.today(),
                                     'issuing_authority': 'New York City',
                                     'issuing_city': 'New York City',
                                     'issuing_country': 'United States of America',
                                     'profile': profile.id,
                                     'file': image},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(Document.objects.all().count(), 1)

    def test_views__add_document__post__should_render_when_form_is_invalid(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.get_profile()
        profile.save()
        document_type: DocumentType = DocumentType(name='Passport', group='ident')
        document_type.save()

        # Act
        response = self.client.post(self.url_add_document,
                                    {'document_type': document_type.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'document.html')
        self.assertNotContains(response, 'alert-success')
        self.assertEquals(Document.objects.all().count(), 0)

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
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_skills, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_skills__get__should_show_selected_skills_when_skills_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
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
        profile: Profile = self.get_profile()
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
        profile: Profile = self.get_profile()
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
        profile: Profile = self.get_profile()
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

    def test_views__add_requested_positions__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/position/')

    def test_views__add_requested_positions__get__should_get_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__add_requested_positions__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__add_requested_positions__get__should_show_selected_positions_when_requested_positions_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.requested_positions.add(Position.objects.filter().first())
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_add_positions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'checked="" class="form-check-input" id="id_requested_positions_')

    def test_views__add_requested_positions__post__should_render_error_when_no_position_is_selected(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.get_profile()
        position = Position.objects.filter().first()
        profile.requested_positions.add(position)
        profile.save()

        # Act
        response = self.client.post(self.url_add_positions,
                                    {},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-danger')
        self.assertEquals(len(profile.skills.all()), 0)

    def test_views__add_requested_position__post__should_render_success_when_2_positions_are_set(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.get_profile()
        position = Position.objects.filter().first()
        profile.save()

        # Act
        response = self.client.post(self.url_add_positions,
                                    {'requested_positions': position.id},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(len(profile.requested_positions.all()), 1)

    def test_views__questions__get__should_redirect_to_login_when_not_logged_in(self):
        # Act
        response = self.client.get(self.url_questions, user=self.user)

        # Assert
        self.assertRedirects(response, '/accounts/login/?next=/accounts/questions/')

    def test_views__questions__get__should_get_403_when_profile_does_not_exist(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_questions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_views__questions__get__should_render_with_form_html_when_profile_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_questions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__questions__get__should_show_existing_answer(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        question = Question.objects.filter().first()
        question.save()
        answer = Answer(text='Answer', profile=profile, question=question)
        answer.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_questions, user=self.user)
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'value="Answer')

    def test_views__questions__post__should_update_answer_when_answer_exists(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        question = Question.objects.filter().first()
        answer = Answer(text='Sample Answer', profile=profile, question=question)
        answer.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_questions,
                                    {'question' + str(question.pk): 'Some answer to a random question!'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEquals(Answer.objects.filter().count(), 1)
        self.assertEquals(Answer.objects.filter().first().text, 'Some answer to a random question!')

    def test_views__questions__post__should_not_create_answer_when_question_is_not_mandatory_and_answer_is_blank(self):
        # Arrange
        profile: Profile = self.get_profile()
        profile.save()
        question_required = Question.objects.filter().first()
        question_optional = Question(text="Question Optional", mandatory=False)
        question_optional.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        data = {'question' + str(question_required.pk): 'Answer Required'}
        response = self.client.post(self.url_questions,
                                    data,
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEquals(Answer.objects.filter().count(), 1)
        self.assertEquals(Answer.objects.filter().first().text, 'Answer Required')

    def test_views__questions__post__should_render_success_when_question_is_answered(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = self.get_profile()
        question = Question.objects.filter().first()
        profile.save()

        # Act
        response = self.client.post(self.url_questions,
                                    {'question' + str(question.pk): 'Some answer to a random question!'},
                                    user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertContains(response, 'alert-success')
        self.assertEquals(len(Answer.objects.all()), 1)

    def get_profile(self) -> Profile:
        return Profile(id=1,
                       user=self.user,
                       first_name='Test',
                       last_name='User',
                       citizenship='Deutsch',
                       date_of_birth=datetime.date.today(),
                       place_of_birth='New York',
                       country_of_birth='United States of America',
                       gender='m',
                       needs_schengen_visa=False,
                       phone='0123456789')
