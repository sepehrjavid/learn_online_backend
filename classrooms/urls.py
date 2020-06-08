from django.urls import path, re_path

from classrooms.views import DeactivateClassAPIView, CreateClassAPIView, UpdateClassAPIView, RetrieveClassAPIView, \
    ListClassAPIView

app_name = "classrooms"

urlpatterns = [
    path('create', CreateClassAPIView.as_view()),
    path('list', ListClassAPIView.as_view()),
    re_path(r'^edit/(?P<pk>\d+)$', UpdateClassAPIView.as_view()),
    re_path(r'^retrieve/(?P<pk>\d+)$', RetrieveClassAPIView.as_view()),
    re_path(r'^deactivate/(?P<pk>\d+)$', DeactivateClassAPIView.as_view()),
]
