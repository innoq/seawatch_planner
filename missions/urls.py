from django.urls import path

from . import views

urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission_list'),
    path('new', views.MissionCreateView.as_view(), name='mission_create'),
    path('<int:pk>/', views.MissionDetailView.as_view(), name='mission_detail'),
    path('<int:pk>/delete', views.MissionDeleteView.as_view(), name='mission_delete'),
    path('ships/', views.ShipListView.as_view(), name='ship_list'),
    path('ships/new', views.ShipCreateView.as_view(), name='ship_create'),
    path('ships/<int:pk>/', views.ShipDetailView.as_view(), name='ship_detail'),
    path('ships/<int:pk>/delete', views.ShipDeleteView.as_view(), name='ship_delete'),
    path('<int:mission__id>/assignments/new', views.AssignmentCreateView.as_view(), name="assignment_create"),
    path('<int:mission__id>/assignments/<int:pk>/delete',
         views.AssignmentDeleteView.as_view(),
         name="assignment_delete"),
    path('<int:mission__id>/assignments/<int:assignment__id>/assignee', views.AssigneeView.as_view(), name="assignee"),
]