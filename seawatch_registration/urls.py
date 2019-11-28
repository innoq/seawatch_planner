from django.urls import path

from seawatch_registration.views.document_create_view import DocumentCreateView
from seawatch_registration.views.document_delete_view import DocumentDeleteView
from seawatch_registration.views.document_list_view import DocumentListView
from seawatch_registration.views.document_update_view import DocumentUpdateView
from seawatch_registration.views.profile_create_view import ProfileCreateView
from seawatch_registration.views.profile_detail_view import ProfileDetailView
from seawatch_registration.views.profile_update_view import ProfileUpdateView
from seawatch_registration.views.question_update_view import QuestionUpdateView
from seawatch_registration.views.requested_position_update_view import RequestedPositionUpdateView
from seawatch_registration.views.signup_view import SignupView
from seawatch_registration.views.skill_update_view import SkillUpdateView

urlpatterns = [
    path('show', ProfileDetailView.as_view(), name='profile_detail'),
    path('add', ProfileCreateView.as_view(), name='profile_create'),
    path('edit', ProfileUpdateView.as_view(), name='profile_update'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('documents/', DocumentListView.as_view(), name='document_list'),
    path('documents/add/', DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:document_id>/edit', DocumentUpdateView.as_view(), name='document_update'),
    path('documents/<int:document_id>/delete', DocumentDeleteView.as_view(), name='document_delete'),
    path('questions/edit', QuestionUpdateView.as_view(), name='question_update'),
    path('requested-positions/edit', RequestedPositionUpdateView.as_view(), name='requested_position_update'),
    path('skills/edit', SkillUpdateView.as_view(), name='skill_update'),
]
