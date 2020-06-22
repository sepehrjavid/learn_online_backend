from django.urls import path, re_path

from classrooms.views import (DeactivateClassAPIView, CreateClassAPIView, UpdateClassAPIView,
                              ListClassAPIView, AddOwnerToClassAPIView, ToggleEnrollClassAPIView,
                              QuitClassOwnershipAPIView)

app_name = "classrooms"

urlpatterns = [
    path('create', CreateClassAPIView.as_view()),
    path('list', ListClassAPIView.as_view()),
    re_path(r'^edit/(?P<pk>\d+)$', UpdateClassAPIView.as_view()),
    re_path(r'^deactivate/(?P<pk>\d+)$', DeactivateClassAPIView.as_view()),
    re_path(r'^add_owner/(?P<pk>\d+)$', AddOwnerToClassAPIView.as_view()),
    re_path(r'^toggle_enrolled/(?P<pk>\d+)$', ToggleEnrollClassAPIView.as_view()),
    re_path(r'^quit_ownership/(?P<pk>\d+)$', QuitClassOwnershipAPIView.as_view()),
]
