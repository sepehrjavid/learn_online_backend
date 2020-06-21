from django.contrib.postgres.fields import JSONField
from django.db import models

from accounting.models import CustomUser
from classrooms.models import Classroom


class Quiz(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT, related_name="quizzes")
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    start_date = models.DateTimeField()
    questions = JSONField()


class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="quiz_answers")
    sent_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    answers = JSONField()
