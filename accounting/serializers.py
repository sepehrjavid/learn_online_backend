from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from accounting.models import CustomUser
from classrooms.serializers import ClassroomBriefSerializer


class UserSerializer(serializers.ModelSerializer):
    joined_classes = ClassroomBriefSerializer(many=True, read_only=True)
    owned_classes = ClassroomBriefSerializer(many=True, read_only=True)
    created_classes = ClassroomBriefSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "password",
            "created_classes",
            "owned_classes",
            "joined_classes"
        ]

        read_only_fields = ("id",)
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        if value <= 5:
            raise ValidationError("You are under aged for signing up")
        return value

    def create(self, validated_data):
        validated_data["username"] = validated_data.get("email")
        return CustomUser.objects.create_user(**validated_data)
