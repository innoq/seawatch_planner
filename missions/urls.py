from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_mission', views.show_mission_editor, name='edit_mission'),
]