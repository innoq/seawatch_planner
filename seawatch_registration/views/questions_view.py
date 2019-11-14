from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic.base import View

from seawatch_registration.forms.dynamic_question_form import DynamicQuestionForm
from seawatch_registration.models import Profile, Question, Answer


class QuestionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(QuestionView, self).__init__()
        self.title = 'Questions'
        self.success_alert = 'Your Answer are successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        questions = list(Question.objects.all())
        answers = Answer.objects.filter(profile=profile)
        return render(request,
                      'form.html',
                      {'form': DynamicQuestionForm(questions=questions, answers=answers),
                       'title': self.title,
                       'success_alert': self.success_alert,
                       'submit_button': self.submit_button})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = DynamicQuestionForm(request.POST, questions=list(Question.objects.all()))
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': request.POST,
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button
                                                 })

        for question in Question.objects.all():
            answer_text = form.cleaned_data['question'+str(question.pk)]
            actual_answers = Answer.objects.filter(profile=profile, question=question)
            if actual_answers.exists():
                actual_answers.delete()
            if answer_text:
                answer = Answer(profile=profile, question=question, text=answer_text)
                answer.save()
        return render(request,
                      'form.html',
                      {'form': DynamicQuestionForm(questions=list(Question.objects.all()),
                                                   answers=Answer.objects.filter(profile=profile)),
                       'success': True,
                       'title': self.title,
                       'success_alert': self.success_alert,
                       'submit_button': self.submit_button
                       })

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()