from django.urls import path

import assessments.views.assessment as assessment

urlpatterns = [
    path('', assessment.ListView.as_view(), name='assessment_list'),
    path('<int:pk>/edit', assessment.UpdateView.as_view(), name='assessment_update'),
]
