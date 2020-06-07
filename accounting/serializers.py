from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from accounting.models import CustomUser


class UserBriefSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name"
        ]

    def get_name(self, obj):
        return obj.first_name + " " + obj.last_name


from classrooms.serializers import ClassroomBriefSerializer


class UserSerializer(serializers.ModelSerializer):
    joined_classes = serializers.SerializerMethodField(read_only=True)
    owned_classes = serializers.SerializerMethodField(read_only=True)
    created_classes = serializers.SerializerMethodField(read_only=True)

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

    def get_created_classes(self, obj):
        return ClassroomBriefSerializer(obj.created_classes.filter(is_active=True), many=True).data

    def get_owned_classes(self, obj):
        return ClassroomBriefSerializer(obj.owned_classes.filter(is_active=True), many=True).data

    def get_joined_classes(self, obj):
        return ClassroomBriefSerializer(obj.joined_classes.filter(is_active=True), many=True).data

    def validate_age(self, value):
        if value <= 5:
            raise ValidationError("You are under aged for signing up")
        return value

    def create(self, validated_data):
        validated_data["username"] = validated_data.get("email")
        return CustomUser.objects.create_user(**validated_data)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name"
        ]
