from django.urls import path
from . import views


urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission-list'),
    path('new', views.MissionCreateView.as_view(), name='mission-create'),
    path('<int:pk>/', views.MissionDetailView.as_view(), name='mission-detail'),
    path('<int:mission__id>/assignments/new', views.AssignmentNewView.as_view(), name="assignment-create"),
    path('<int:mission__id>/assignments/<int:assignment__id>', views.AssignmentView.as_view(), name="assignment"),
    path('<int:mission__id>/assignments/<int:assignment__id>/assignee', views.AssigneeView.as_view(), name="assignee"),
]