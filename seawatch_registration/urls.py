from django.urls import path

import seawatch_registration.views.document as document
import seawatch_registration.views.position as position
import seawatch_registration.views.profile as profile
import seawatch_registration.views.question as question
import seawatch_registration.views.skill as skill
from seawatch_registration.views.signup import SignupView

urlpatterns = [
    path('show', profile.DetailView.as_view(), name='profile_detail'),
    path('add', profile.CreateView.as_view(), name='profile_create'),
    path('edit', profile.UpdateView.as_view(), name='profile_update'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('documents/', document.ListView.as_view(), name='document_list'),
    path('documents/add/', document.CreateView.as_view(), name='document_create'),
    path('documents/<int:document_id>/edit', document.UpdateView.as_view(), name='document_update'),
    path('documents/<int:document_id>/delete', document.DeleteView.as_view(), name='document_delete'),
    path('questions/edit', question.UpdateView.as_view(), name='question_update'),
    path('positions/edit', position.UpdateView.as_view(), name='requested_position_update'),
    path('skills/edit', skill.UpdateView.as_view(), name='skill_update'),
]
