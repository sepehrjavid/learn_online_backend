from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.response import Response

from classrooms.models import Classroom
from classrooms.permissions import (IsClassroomCreatorPermission, IsClassroomOwnerPermission, IsClassMemberPermission)
from quizzes.models import Quiz, QuizAnswer
from quizzes.permissions import CanSubmitAnswerPermission
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


class CreateQuizAPIView(CreateAPIView):
    permission_classes = [IsClassroomCreatorPermission | IsClassroomOwnerPermission]
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def perform_create(self, serializer):
        classroom = get_object_or_404(Classroom, id=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, classroom)
        serializer.save(classroom=classroom)


class AnswerQuizAPIView(CreateAPIView):
    permission_classes = [CanSubmitAnswerPermission]
    serializer_class = QuizAnswerSerializer
    queryset = QuizAnswer.objects.all()

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, id=self.kwargs.get("pk"))
        self.check_object_permissions(self.request, quiz)
        serializer.save(quiz=quiz, user=self.request.user)
