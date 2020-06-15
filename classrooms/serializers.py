from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounting.models import CustomUser
from classrooms.models import Classroom
from accounting.serializers import UserBriefSerializer


class ClassroomBriefSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    other_owners = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "creator",
            "description",
            "other_owners",
            "is_online"
        ]

    def get_creator(self, obj):
        return UserBriefSerializer(obj.creator).data

    def get_other_owners(self, obj):
        return UserBriefSerializer(obj.other_owners, many=True).data


class ClassroomCreateSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    other_owners_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "description",
            "creator",
            "other_owners",
            "other_owners_data",
            "enrolled"
        ]

        read_only_fields = ("id", "creator", "enrolled")
        extra_kwargs = {"other_owners_data": {"write_only": True}}

    def get_creator(self, obj):
        return UserBriefSerializer(obj.creator).data

    def get_other_owners_data(self, obj):
        return UserBriefSerializer(obj.other_owners, many=True).data

    def validate_other_owners(self, value):
        request = self.context.get("request")

        for user in value:
            if request.user == user:
                raise ValidationError("Can't have yourself as other owners")

        return value


class ClassroomEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "description",
        ]


class AddOwnerToClassSerializer(serializers.Serializer):
    owners = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate_owners(self, value):
        request = self.context.get("request")

        for user in value:
            if request.user == user:
                raise ValidationError("Can't have yourself as other owners")

        return value
