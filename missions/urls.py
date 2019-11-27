from django.urls import path

from . import views

urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission-list'),
    path('new', views.MissionCreateView.as_view(), name='mission-create'),
    path('<int:pk>/', views.MissionDetailView.as_view(), name='mission-detail'),
    path('<int:pk>/delete', views.MissionDeleteView.as_view(), name='mission-delete'),
    path('ships/', views.ShipListView.as_view(), name='ship-list'),
    path('ships/new', views.ShipCreateView.as_view(), name='ship-create'),
    path('ship/<int:pk>/', views.ShipDetailView.as_view(), name='ship-detail'),
    path('ship/<int:pk>/delete', views.ShipDeleteView.as_view(), name='ship-delete'),
    path('<int:mission__id>/assignments/new', views.AssignmentCreateView.as_view(), name="assignment-create"),
    path('<int:mission__id>/assignment/<int:pk>/delete',
         views.AssignmentDeleteView.as_view(),
         name="assignment-delete"),
    path('<int:mission__id>/assignment/<int:assignment__id>/assignee', views.AssigneeView.as_view(), name="assignee"),
]