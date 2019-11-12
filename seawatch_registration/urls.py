from django.urls import path

from seawatch_registration.views import RequestedPositionView
from . import views

urlpatterns = [
    path('show/', views.show_profile, name='show_profile'),
    path('add/', views.add_profile, name='add_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('signup/', views.signup, name='signup'),
    path('document/add/', views.add_document, name='add_document'),
    path('position/', RequestedPositionView.as_view(), name='requested_profile'),
]
