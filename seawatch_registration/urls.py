from django.urls import path

from seawatch_registration.views import (
    availability, document, position, profile, question, registration_process, skill, signup, signin)

urlpatterns = [
    path('profile/show/', profile.DetailView.as_view(), name='profile_detail'),
    path('profile/add/', profile.CreateView.as_view(), name='profile_create'),
    path('profile/edit/', profile.UpdateView.as_view(), name='profile_update'),
    path('signup/', signup.SignupView.as_view(), name='signup'),
    path('login/success/', signin.login_success, name='login_success'),
    path('documents/', document.ListView.as_view(), name='document_list'),
    path('documents/add/', document.CreateView.as_view(), name='document_create'),
    path('documents/<int:document_id>/edit', document.UpdateView.as_view(), name='document_update'),
    path('documents/<int:document_id>/delete', document.DeleteView.as_view(), name='document_delete'),
    path('documents/<int:document_id>/<str:file_name>', document.GetDocumentAttachment.as_view(),
         name='document_attachment_get'),
    path('questions/edit/', question.UpdateView.as_view(), name='question_answer'),
    path('positions/edit/', position.UpdateView.as_view(), name='requested_position_update'),
    path('skills/edit/', skill.UpdateView.as_view(), name='skill_update'),
    path('availabilities/', availability.ListView.as_view(), name='availability_list'),
    path('availabilities/add/', availability.CreateView.as_view(), name='availability_create'),
    path('registration/', registration_process.View.as_view(), name='registration_process'),
]
