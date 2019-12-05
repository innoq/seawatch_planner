from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from seawatch_registration.models import Question


class CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Question
    fields = ['text', 'mandatory']
    nav_item = 'questions'
    success_url = reverse_lazy('question_list')
    permission_required = 'seawatch_registration.add_question'


class ListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Question
    paginate_by = 10
    nav_item = 'questions'
    permission_required = 'seawatch_registration.view_question'


class DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Question
    nav_item = 'questions'
    success_url = reverse_lazy('question_list')
    permission_required = 'seawatch_registration.delete_question'


class UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Question
    fields = ['text', 'mandatory']
    success_url = reverse_lazy('question_list')
    permission_required = 'seawatch_registration.change_question'


