from django.urls import re_path

from quizzes.views import GetClassQuizzesAPIView, GetQuizAnswersAPIView

app_name = "quizzes"

urlpatterns = [
    re_path(r'^retrieve/(?P<pk>\d+)', GetClassQuizzesAPIView.as_view()),
    re_path(r'^quiz_answers/(?P<pk>\d+)', GetQuizAnswersAPIView.as_view())
]
