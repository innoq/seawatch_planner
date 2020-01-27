from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import CharField, Form, Textarea
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from seawatch_registration.mixins import HasProfileMixin, RegistrationStepOrderMixin
from seawatch_registration.models import Answer, Question


class DynamicQuestionForm(Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        answers = kwargs.pop('answers', None)
        super(DynamicQuestionForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields['question' + str(question.pk)] = \
                CharField(label=question.text, max_length=1000, required=question.mandatory, widget=Textarea)
            if answers:
                answer = answers.filter(question=question).first()
                if answer:
                    self.fields['question' + str(question.pk)].initial = answer.text


class AnsweringQuestionsView(LoginRequiredMixin, SuccessMessageMixin,
                             RegistrationStepOrderMixin, HasProfileMixin,
                             FormView):
    nav_item = 'questions'
    title = _('Questions')
    success_message = _('Your answer has been saved.')
    success_url = reverse_lazy('question_answer')
    error_message = _('Your answers could not be saved.')
    submit_button = _('Next')
    form_class = DynamicQuestionForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(),
                'questions': list(Question.objects.all()),
                'answers': Answer.objects.filter(profile=self.request.user.profile)}

    def form_valid(self, form):
        self._save_all_answers(form)
        return super().form_valid(form)

    def _save_all_answers(self, form):
        profile = self.request.user.profile
        for question in Question.objects.all():
            answer_text = form.cleaned_data['question' + str(question.pk)]
            if answer_text.strip():
                Answer.objects.update_or_create(
                    profile=profile, question=question,
                    defaults={'text': answer_text})
            else:
                Answer.objects.filter(profile=profile, question=question).delete()
