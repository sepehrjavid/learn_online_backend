from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounting.models import CustomUser
from classrooms.models import Classroom
from accounting.serializers import UserBriefSerializer


class ClassroomBriefSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "creator",
            "description",
            "is_online"
        ]

    def get_creator(self, obj):
        return UserBriefSerializer(obj.creator).data


class ClassroomSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "description",
            "creator",
            "other_owners",
            "enrolled"
        ]

        read_only_fields = ("id", "creator", "enrolled")

    def get_creator(self, obj):
        return UserBriefSerializer(obj.creator).data

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


class ClassroomRetrieveSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    other_owners = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "description",
            "creator",
            "other_owners",
        ]

    def get_creator(self, obj):
        return UserBriefSerializer(obj.creator).data

    def get_other_owners(self, obj):
        return UserBriefSerializer(obj.other_owners, many=True).data


class AddOwnerToClassSerializer(serializers.Serializer):
    owners = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
