from django.urls import path

import missions.views.assignment as assignment
import missions.views.mission as mission
import missions.views.ship as ship

urlpatterns = [
    path('', mission.ListView.as_view(), name='mission_list'),
    path('new', mission.CreateView.as_view(), name='mission_create'),
    path('<int:pk>/', mission.DetailView.as_view(), name='mission_detail'),
    path('<int:pk>/delete', mission.DeleteView.as_view(), name='mission_delete'),
    path('ships/', ship.ListView.as_view(), name='ship_list'),
    path('ships/new', ship.CreateView.as_view(), name='ship_create'),
    path('ships/<int:pk>/', ship.DetailView.as_view(), name='ship_detail'),
    path('ships/<int:pk>/delete', ship.DeleteView.as_view(), name='ship_delete'),
    path('<int:mission__id>/assignments/new', assignment.CreateView.as_view(), name="assignment_create"),
    path('<int:mission__id>/assignments/<int:pk>/delete',
         assignment.DeleteView.as_view(),
         name="assignment_delete"),
    path('<int:mission__id>/assignments/<int:assignment__id>/assignee',
         assignment.UpdateView.as_view(),
         name="assignee"),
]
