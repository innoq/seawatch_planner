from django.urls import path

from assessments.views.assessment_view import AssessmentView
from assessments.views.assessments_view import AssessmentOverviewView

urlpatterns = [
    path('', AssessmentOverviewView.as_view(), name='assessments'),
    path('<int:profile_id>/', AssessmentView.as_view(), name='assessment'),
]