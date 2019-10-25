from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_profile),
    path('edit/', views.edit_profile),
    path('signup/', views.signup),
]
