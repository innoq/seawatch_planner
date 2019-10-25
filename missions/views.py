from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View

from .forms import AssignmentForm
from .models import Mission, Assignment

class MissionListView(ListView):

    model = Mission
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MissionCreateView(CreateView):
    model = Mission
    fields = ['name', 'start_date', 'end_date', 'ship']

    def get_success_url(self):
        return reverse('mission-detail', kwargs={'id': self.object.id})

class MissionDetailView(DetailView):
    model = Mission

class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ['position']

    def __init__(self, *args, **kwargs):
        self.mission_id = kwargs.pop('mission__id', None)
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
         form.instance.mission_id = self.mission_id
         return super(AssignmentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mission-detail', kwargs={'id': self.mission.object.id})

class AssignmentView(View):
    def delete(self, request, *args, **kwargs):
        print("DELETE")
        assignment = get_object_or_404(Assignment, pk=kwargs.pop('assignment__id'), mission_id=kwargs.pop('mission__id'))
        assignment.delete()

class AssigneeView(View):
    pass

class AssignmentNewView(View):
    form_class = AssignmentForm
    initial = {'key': 'value'}
    template_name = 'missions/assignment_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        mission = get_object_or_404(Mission, pk=kwargs.pop('mission__id'))
        if form.is_valid():
            form.instance.mission_id = mission.id
            form.save()
            return redirect(reverse('mission-detail', kwargs={'pk': mission.id}))
        return render(request, self.template_name, {'form': form})


