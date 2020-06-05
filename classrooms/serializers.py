from rest_framework import serializers

from classrooms.models import Classroom


class ClassroomBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "id",
            "name",
            "creator"
        ]
