from rest_framework import serializers

from classrooms.models import Classroom


class ClassroomBriefSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "creator",
            "is_online"
        ]

    def get_creator(self, obj):
        return {"id": obj.creator.id, "name": obj.creator.first_name + " " + obj.creator.last_name}
