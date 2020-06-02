from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from accounting.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "password"
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
