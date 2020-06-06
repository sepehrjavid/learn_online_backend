from django.urls import path, re_path

from classrooms.views import DeactivateClassAPIView

app_name = "classrooms"

urlpatterns = [
    re_path(r'^deactivate/(?P<pk>\d+)$', DeactivateClassAPIView.as_view())
]
