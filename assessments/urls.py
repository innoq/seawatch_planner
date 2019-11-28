from django.urls import path

from assessments.views.assessment_list_view import AssessmentListView
from assessments.views.assessment_view import AssessmentUpdateView

urlpatterns = [
    path('', AssessmentListView.as_view(), name='assessment_list'),
    path('<int:profile_id>/edit', AssessmentUpdateView.as_view(), name='assessment_update'),
]
