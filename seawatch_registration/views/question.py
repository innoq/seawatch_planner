from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import FormView

from seawatch_registration.forms.dynamic_question_form import \
    DynamicQuestionForm
from seawatch_registration.mixins import HasProfileMixin
from seawatch_registration.models import Answer, Question


class UpdateView(LoginRequiredMixin, HasProfileMixin, FormView):
    nav_item = 'questions'
    title = 'Questions'
    success_alert = 'Your answer has been saved.'
    error_message = 'Your answers could not be saved.'
    submit_button = 'Next'
    form_class = DynamicQuestionForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(),
                'questions': list(Question.objects.all()),
                'answers': Answer.objects.filter(profile=self.request.user.profile)}

    def form_valid(self, form):
        self._save_all_answers(form)
        redirect_to = self.request.GET.get('next')
        if redirect_to:
            return redirect(redirect_to)
        return render(self.request, 'form.html', {'form': form, 'success': True, 'view': self})

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
