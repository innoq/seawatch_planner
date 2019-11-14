from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from seawatch_registration.models import Profile, Question, Answer
from seawatch_registration.tests.views import util


class TestQuestionsView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.username = 'testuser1'
        self.password = '1X<ISRUkw+tuK'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        self.url_questions = reverse('questions')

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
        profile: Profile = util.get_profile(self.user)
        profile.save()
        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.get(self.url_questions, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

    def test_views__questions__get__should_show_existing_answer(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
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
        profile: Profile = util.get_profile(self.user)
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
        profile: Profile = util.get_profile(self.user)
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

    def test_views__questions__post__should_not_update_answer_when_question_is_mandatory_and_answer_is_blank(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        question = Question.objects.filter().first()
        answer = Answer(text="Example Answer", profile=profile, question=question)
        answer.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_questions, {}, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEquals(Answer.objects.filter().count(), 1)
        self.assertEquals(Answer.objects.filter().first().text, 'Example Answer')

    def test_views__questions__post__should_not_add_answer_when_question_is_mandatory_and_answer_is_blank(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()

        self.client.login(username=self.username, password=self.password)

        # Act
        response = self.client.post(self.url_questions, {}, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEquals(Answer.objects.filter().count(), 0)

    def test_views__questions__post__should_remove_optional_answer_when_no_answer_for_question_is_sent(self):
        # Arrange
        profile: Profile = util.get_profile(self.user)
        profile.save()
        question_required = Question.objects.filter().first()
        question_optional = Question(text="Question Optional", mandatory=False)
        question_optional.save()
        answer_required = Answer(text="Answer required", question=question_required, profile=profile)
        answer_required.save()
        answer_optional = Answer(text="Answer optional", question=question_optional, profile=profile)
        answer_optional.save()

        self.client.login(username=self.username, password=self.password)
        data = {'question' + str(question_required.pk): 'Answer required new'}

        # Act
        response = self.client.post(self.url_questions, data, user=self.user)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertEquals(Answer.objects.all().count(), 1)
        self.assertEquals(Answer.objects.all().first().text, 'Answer required new')

    def test_views__questions__post__should_render_success_when_question_is_answered(self):
        # Arrange
        self.client.login(username=self.username, password=self.password)
        profile: Profile = util.get_profile(self.user)
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
