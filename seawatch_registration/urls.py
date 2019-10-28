from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show_profile),
    path('add/', views.add_profile),
    path('edit/', views.edit_profile),
    path('signup/', views.signup),
    path('position/', views.profileposition_form),
]
