from django.contrib import admin
from django.urls import include, path

from seawatch_registration.views.index import IndexView

urlpatterns = [
    path('missions/', include('missions.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('seawatch_registration.urls')),
    path('assessments/', include('assessments.urls')),
    path('', IndexView.as_view(), name='index')
]
