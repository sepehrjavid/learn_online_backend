from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from classrooms.models import Classroom
from classrooms.permissions import (IsClassroomCreatorPermission, IsClassroomOwnerPermission, IsClassMemberPermission)
from quizzes.models import Quiz, QuizAnswer
from quizzes.serializers import QuizSerializer, QuizAnswerSerializer


class GetClassQuizzesAPIView(ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(classroom__id=self.kwargs.get("pk"))


class GetQuizAnswersAPIView(ListAPIView):
    serializer_class = QuizAnswerSerializer
    permission_classes = [IsClassMemberPermission]

    def get_object(self):
        obj = get_object_or_404(Classroom, id=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        classroom = self.get_object()
        return QuizAnswer.objects.filter(quiz__classroom=classroom, user=self.request.user)
