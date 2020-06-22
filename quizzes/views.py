from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response

from classrooms.models import Classroom
from classrooms.permissions import (IsClassroomCreatorPermission, IsClassroomOwnerPermission, IsClassMemberPermission)
from quizzes.models import Quiz, QuizAnswer
from quizzes.permissions import CanSubmitAnswerPermission
from quizzes.serializers import QuizSerializer, QuizAnswerSerializer, QuizBriefSerializer


class GetClassQuizzesAPIView(ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(classroom__id=self.kwargs.get("pk"))


class GetQuizOwnAnswersAPIView(GenericAPIView):
    serializer_class = QuizAnswerSerializer
    permission_classes = [IsClassMemberPermission]
    queryset = Classroom.objects.all()

    def get(self, request, pk):
        classroom = self.get_object()
        answered = QuizAnswer.objects.filter(quiz__classroom=classroom, user=self.request.user).order_by("-sent_date")
        answered_quiz_id = [x.quiz.id for x in answered]
        not_answered_quiz = Quiz.objects.filter(classroom=classroom).exclude(id__in=answered_quiz_id).order_by(
            "deadline")
        result = {
            "answered": QuizAnswerSerializer(answered, many=True).data,
            "not_answered": QuizBriefSerializer(not_answered_quiz, many=True).data
        }
        return Response(result, status=status.HTTP_200_OK)


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
