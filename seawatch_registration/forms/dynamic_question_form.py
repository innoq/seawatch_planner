from django.forms import Form, CharField, Textarea


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
