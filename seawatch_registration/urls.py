from django.urls import path

from seawatch_registration.views import RequestedPositionView, AddSkillsView
from . import views

urlpatterns = [
    path('show/', views.show_profile),
    path('add/', views.add_profile),
    path('edit/', views.edit_profile),
    path('signup/', views.signup),
    path('document/', views.document_form),
    path('position/', RequestedPositionView.as_view(), name='requested_profile'),
    path('skill/', AddSkillsView.as_view(), name='skill')
]
