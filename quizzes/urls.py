from django.urls import re_path

from quizzes.views import GetClassQuizzesAPIView, GetQuizOwnAnswersAPIView, CreateQuizAPIView, AnswerQuizAPIView

app_name = "quizzes"

urlpatterns = [
    re_path(r'^retrieve/(?P<pk>\d+)', GetClassQuizzesAPIView.as_view()),  # classroom pk
    re_path(r'^quiz_answers/(?P<pk>\d+)', GetQuizOwnAnswersAPIView.as_view()),  # classroom pk
    re_path(r'^create/(?P<pk>\d+)', CreateQuizAPIView.as_view()),  # classroom pk
    re_path(r'^answer/(?P<pk>\d+)', AnswerQuizAPIView.as_view()),  # quiz pk
]
