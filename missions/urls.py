from django.urls import path

import missions.views.assignment as assignment
import missions.views.default_assigments as default_assignments
import missions.views.mission as mission
import missions.views.ship as ship
from missions.views import question

urlpatterns = [
    path('', mission.ListView.as_view(), name='mission_list'),
    path('new', mission.CreateView.as_view(), name='mission_create'),
    path('<int:pk>/', mission.DetailView.as_view(), name='mission_detail'),
    path('<int:pk>/delete', mission.DeleteView.as_view(), name='mission_delete'),
    path('<int:pk>/edit', mission.UpdateView.as_view(), name='mission_update'),
    path('ships/', ship.ListView.as_view(), name='ship_list'),
    path('ships/new', ship.CreateView.as_view(), name='ship_create'),  # TODO: Replace 'new' with 'add'
    path('ships/<int:pk>/edit/', ship.UpdateView.as_view(), name='ship_update'),
    path('ships/<int:pk>/delete/', ship.DeleteView.as_view(), name='ship_delete'),
    path('ships/<int:ship_id>/default-assignments/',
         default_assignments.ListView.as_view(),
         name='default_assignment_list'),
    path('ships/<int:ship_id>/default-assignments/add/',
         default_assignments.CreateView.as_view(),
         name='default_assignment_create'),
    path('ships/<int:ship_id>/default-assignments/<int:pk>/edit/',
         default_assignments.UpdateView.as_view(),
         name='default_assignment_update'),
    path('ships/<int:ship_id>/default-assignments/<int:pk>/delete',
         default_assignments.DeleteView.as_view(),
         name='default_assignment_delete'),
    path('<int:mission__id>/assignments/new', assignment.CreateView.as_view(), name="assignment_create"),
    path('<int:mission__id>/assignments/<int:pk>/delete',
         assignment.DeleteView.as_view(),
         name="assignment_delete"),
    path('<int:mission__id>/assignments/<int:pk>/send_mail',
         assignment.EmailView.as_view(),
         name="assignment_mail"),
    path('<int:mission__id>/assignments/<int:assignment__id>/assignee',
         assignment.UpdateView.as_view(),
         name="assignee"),
    path('questions/', question.ListView.as_view(), name='question_list'),
    path('questions/add', question.CreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/delete', question.DeleteView.as_view(), name='question_delete'),
    path('questions/<int:pk>/edit', question.UpdateView.as_view(), name='question_update'),

]
