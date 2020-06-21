import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from learn_online_backend.settings import QUESTION_TYPES, MULTIPLE_CHOICE, TRUE_OR_FALSE, DESCRIPTIVE
from quizzes.models import Quiz, QuizAnswer


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "created_date",
            "deadline",
            "start_date",
            "questions"
        ]

        read_only_fields = ("id",)

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
                for choice in question.get("choices"):
                    if type(choice) != str:
                        raise ValidationError("Choices must be string")
        return questions

    def validate(self, attrs):
        now = datetime.datetime.now()
        if now > attrs.get("start_date"):
            raise ValidationError("Start date cannot be before current time")
        if attrs.get("start_date") >= attrs.get("deadline"):
            raise ValidationError("Deadline cannot be before or at the same time as start date")
        return attrs


class QuizAnswerSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)

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

    def validate_answers(self, answers):
        question_id = self.context.get("view").kwargs.get("pk")
        questions = get_object_or_404(Quiz, id=question_id).questions
        if len(answers) != len(questions):
            raise ValidationError("number of Answers is not equal to number of questions")
        for i in range(len(answers)):
            if questions[i]["type"] == MULTIPLE_CHOICE:
                if answers[i] not in questions[i]["choices"]:
                    raise ValidationError("Invalid choice answer")
                if type(answers[i]) != str:
                    raise ValidationError("Choice answer must be string")
            if questions[i]["type"] == TRUE_OR_FALSE and type(answers[i]) != bool:
                raise ValidationError("True or false answer should be boolean")
            if questions[i]["type"] == DESCRIPTIVE and type(answers[i]) != str:
                raise ValidationError("Descriptive answer must be string")

        return answers
