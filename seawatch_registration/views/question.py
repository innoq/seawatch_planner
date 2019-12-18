from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.forms.dynamic_question_form import DynamicQuestionForm
from seawatch_registration.models import Profile, Question, Answer


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    nav_item = 'questions'
    title = 'Questions'
    success_alert = 'Your answer has been saved.'
    submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        questions = list(Question.objects.all())
        answers = Answer.objects.filter(profile=profile)
        return render(request,
                      'form.html',
                      {'form': DynamicQuestionForm(questions=questions, answers=answers),
                       'view': self})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = DynamicQuestionForm(request.POST, questions=list(Question.objects.all()))
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': request.POST,
                                                 'view': self})

        for question in Question.objects.all():
            answer_text = form.cleaned_data['question'+str(question.pk)]
            actual_answers = Answer.objects.filter(profile=profile, question=question)
            if actual_answers.exists():
                actual_answers.delete()
            if answer_text:
                answer = Answer(profile=profile, question=question, text=answer_text)
                answer.save()

        redirect_to = self.request.GET.get('next')
        if redirect_to:
            return redirect(redirect_to)

        return render(request,
                      'form.html',
                      {'form': DynamicQuestionForm(questions=list(Question.objects.all()),
                                                   answers=Answer.objects.filter(profile=profile)),
                       'success': True,
                       'view': self})

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()
