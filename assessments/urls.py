from django.urls import path

from assessments.views import assessment

urlpatterns = [
    path('', assessment.ListView.as_view(), name='assessment_list'),
    path('<int:pk>/edit', assessment.UpdateView.as_view(), name='assessment_update'),
]
