from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.base import View

from seawatch_registration.models import Profile, Question, Answer
from seawatch_registration.forms import DocumentForm, ProfileForm, SignupForm, RequestedPositionForm, SkillsForm, \
    DynamicQuestionForm


@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('add_profile')

    form = ProfileForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('show_profile')

    return render(request, 'profile.html', {'form': form})


@login_required
def add_profile(request):
    form = ProfileForm({'user': request.user})

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/show/')

    return render(request, 'profile.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('add_profile')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def has_profile(user):
    return Profile.objects.filter(user=user).exists()


@login_required
def show_profile(request):
    if not has_profile(request.user):
        return redirect('add_profile')
    profile = request.user.profile
    return render(request, 'show-profile.html', {'profile': profile})


@login_required
def add_document(request):
    if not has_profile(request.user):
        return redirect('add_profile')
    form = DocumentForm(user=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return render(request,
                          'document.html',
                          {'form': DocumentForm(user=request.user), 'success': True})
    return render(request, 'document.html', {'form': form})


class AddSkillsView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(AddSkillsView, self).__init__()
        self.title = 'Add Skills'
        self.success_alert = 'Skills are successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        return render(request, 'form.html', {'form': SkillsForm(profile=profile),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = SkillsForm(request.POST, profile=profile)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': 'Choose at least one skill.',
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button
                                                 })
        languages = form.cleaned_data['languages']
        skills = form.cleaned_data['skills']
        profile.skills.clear()
        for skill in skills:
            profile.skills.add(skill)
        for language in languages:
            profile.skills.add(language)
        return render(request,
                      'form.html',
                      {'form': SkillsForm(profile=profile),
                       'success': True,
                       'title': self.title,
                       'success_alert': self.success_alert,
                       'submit_button': self.submit_button
                       })

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


class RequestedPositionView(LoginRequiredMixin, UserPassesTestMixin, View):

    def __init__(self):
        super(RequestedPositionView, self).__init__()
        self.title = 'Add Requested Position'
        self.success_alert = 'Requested Positions are successfully saved!'
        self.submit_button = 'Next'

    def get(self, request, *args, **kwargs):
        return render(request, 'form.html', {'form': RequestedPositionForm(user=request.user),
                                             'title': self.title,
                                             'success_alert': self.success_alert,
                                             'submit_button': self.submit_button})

    def post(self, request, *args, **kwargs):
        form = RequestedPositionForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(request, 'form.html', {'form': form,
                                                 'error': 'Choose at least one position.',
                                                 'title': self.title,
                                                 'success_alert': self.success_alert,
                                                 'submit_button': self.submit_button
                                                 })
        profile = Profile.objects.get(user=request.user)
        requested_positions = form.cleaned_data['requested_positions']
        profile.requested_positions.clear()
        for position in requested_positions:
            profile.requested_positions.add(position)
        return render(request,
                      'form.html',
                      {'form': RequestedPositionForm(user=request.user),
                       'success': True,
                       'title': self.title,
                       'success_alert': self.success_alert,
                       'submit_button': self.submit_button
                       })

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()


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
            if 'question'+str(question.pk) in form.cleaned_data.keys():
                answer_text = form.cleaned_data['question'+str(question.pk)]
                if answer_text:
                    actual_answers = Answer.objects.filter(profile=profile, question=question)
                    if actual_answers.exists():
                        actual_answers.delete()
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
