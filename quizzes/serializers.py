from rest_framework import serializers

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
