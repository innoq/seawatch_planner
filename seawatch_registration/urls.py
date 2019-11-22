from django.urls import path

from seawatch_registration.views.add_document_view import AddDocumentView
from seawatch_registration.views.add_profile_view import AddProfileView
from seawatch_registration.views.add_skills_view import AddSkillsView
from seawatch_registration.views.delete_document_view import DeleteDocumentView
from seawatch_registration.views.document_list_view import DocumentListView
from seawatch_registration.views.edit_document_view import DocumentUpdateView
from seawatch_registration.views.edit_profile_view import EditProfileView
from seawatch_registration.views.questions_view import QuestionView
from seawatch_registration.views.requested_positions_view import RequestedPositionView
from seawatch_registration.views.show_profile_view import ShowProfileView
from seawatch_registration.views.signup_view import SignupView

urlpatterns = [
    path('show/', ShowProfileView.as_view(), name='show_profile'),
    path('add/', AddProfileView.as_view(), name='add_profile'),
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('documents/', DocumentListView.as_view(), name='document_list'),
    path('document/add/', AddDocumentView.as_view(), name='add_document'),
    path('document/<int:document_id>/', DocumentUpdateView.as_view(), name='edit_document'),
    path('document/<int:document_id>/delete/', DeleteDocumentView.as_view(), name='delete_document'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('position/', RequestedPositionView.as_view(), name='add_requested_profile'),
    path('skills/', AddSkillsView.as_view(), name='add_skills'),
]
