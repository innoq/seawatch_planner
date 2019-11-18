from django.urls import path

from seawatch_registration.views.add_document_view import AddDocumentView
from seawatch_registration.views.add_profile_view import AddProfileView
from seawatch_registration.views.add_skills_view import AddSkillsView
from assessments.views.assessment_view import AssessmentView
from seawatch_registration.views.edit_profile_view import EditProfileView
from seawatch_registration.views.questions_view import QuestionView
from seawatch_registration.views.requested_positions_view import RequestedPositionView
from assessments.views.assessments_view import AssessmentOverviewView
from seawatch_registration.views.show_profile_view import ShowProfileView
from seawatch_registration.views.signup_view import SignupView

urlpatterns = [
    path('show/', ShowProfileView.as_view(), name='show_profile'),
    path('add/', AddProfileView.as_view(), name='add_profile'),
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('document/add/', AddDocumentView.as_view(), name='add_document'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('position/', RequestedPositionView.as_view(), name='add_requested_profile'),
    path('skills/', AddSkillsView.as_view(), name='add_skills'),
    path('assessments/', AssessmentOverviewView.as_view(), name='assessments'),
    path('assessments/<int:profile_id>/', AssessmentView.as_view(), name='assessment'),
]
