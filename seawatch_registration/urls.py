from django.contrib.auth.decorators import login_required
from django.urls import path

from seawatch_registration.views import RequestedPositionView
from . import views

urlpatterns = [
    path('show/', views.show_profile),
    path('add/', views.add_profile),
    path('edit/', views.edit_profile),
    path('signup/', views.signup),
    path('position/', RequestedPositionView.as_view(), name='requested_profile'),
]
