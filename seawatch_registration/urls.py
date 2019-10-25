from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_form),
    path('signup/', views.signup),
]
