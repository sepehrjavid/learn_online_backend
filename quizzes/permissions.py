from rest_framework.permissions import BasePermission


class CanSubmitAnswerPermission(BasePermission):
    message = "you cannot submit answer for this quiz. you need to enroll first"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.classroom.enrolled.all()
