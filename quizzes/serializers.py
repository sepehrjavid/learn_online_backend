import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounting.serializers import UserBriefSerializer
from learn_online_backend.settings import QUESTION_TYPES, MULTIPLE_CHOICE, TRUE_OR_FALSE, DESCRIPTIVE
from quizzes.models import Quiz, QuizAnswer


class QuizAnswerBriefSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer()

    class Meta:
        model = QuizAnswer
        fields = [
            "id",
            "user",
            "sent_date",
            "score",
            "answers",
        ]


class QuizSerializer(serializers.ModelSerializer):
    answers = QuizAnswerBriefSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "created_date",
            "answers",
            "deadline",
            "start_date",
            "questions"
        ]

        read_only_fields = ("id", "created_date")

    def validate_questions(self, questions):
        if len(questions) == 0:
            raise ValidationError("Questions cannot be empty")
        for question in questions:
            keys = question.keys()
            if 'text' not in keys:
                raise ValidationError("Text of the question is not included")
            if 'type' not in keys:
                raise ValidationError("Type of the question is not specified")
            if question.get("type") not in QUESTION_TYPES.keys():
                raise ValidationError("Invalid question type")
            if QUESTION_TYPES[question.get("type")] == MULTIPLE_CHOICE:
                if 'choices' not in keys:
                    raise ValidationError("Choices of multiple choice question are not included")
                if type(question.get("choices")) != list:
                    raise ValidationError("Invalid structure for choices")
                for choice in question.get("choices"):
                    if type(choice) != str:
                        raise ValidationError("Choices must be string")
        return questions

    def validate(self, attrs):
        now = datetime.datetime.now()
        now = now.replace(tzinfo=datetime.timezone.utc)
        if now > attrs.get("start_date"):
            raise ValidationError("Start date cannot be before current time")
        if attrs.get("start_date") >= attrs.get("deadline"):
            raise ValidationError("Deadline cannot be before or at the same time as start date")
        return attrs


class QuizBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "deadline",
            "start_date",
            "questions"
        ]


class QuizAnswerSerializer(serializers.ModelSerializer):
    quiz = QuizBriefSerializer(read_only=True)

    class Meta:
        model = QuizAnswer
        fields = [
            "id",
            "quiz",
            "sent_date",
            "score",
            "answers",
        ]
        read_only_fields = ("id", "score", "sent_date")

    def validate(self, attrs):
        user = self.context.get("request").user
        quiz_id = self.context.get("view").kwargs.get("pk")
        qs = QuizAnswer.objects.filter(user=user, quiz_id=quiz_id)
        if qs.exists():
            raise ValidationError("You already have answered this quiz")
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if quiz.start_date > datetime.datetime.now().replace(tzinfo=datetime.timezone.utc):
            raise ValidationError("Quiz has not started yet")
        return attrs

    def validate_answers(self, answers):
        quiz_id = self.context.get("view").kwargs.get("pk")
        questions = get_object_or_404(Quiz, id=quiz_id).questions
        if len(answers) != len(questions):
            raise ValidationError("number of Answers is not equal to number of questions")
        for i in range(len(answers)):
            if questions[i]["type"] == MULTIPLE_CHOICE:
                if answers[i] not in questions[i]["choices"]:
                    raise ValidationError("Invalid choice answer")
                if type(answers[i]) != str:
                    raise ValidationError("Choice answer must be string")
            if questions[i]["type"] == TRUE_OR_FALSE and type(answers[i]) != bool and answers[i] is not None:
                raise ValidationError("True or false answer should be boolean")
            if questions[i]["type"] == DESCRIPTIVE and type(answers[i]) != str:
                raise ValidationError("Descriptive answer must be string")

        return answers
