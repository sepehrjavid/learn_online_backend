from rest_framework.permissions import BasePermission


class IsClassroomCreatorPermission(BasePermission):
    message = "you are not the creator of the class"

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsClassroomOwnerPermission(BasePermission):
    message = "you are not an owner of the class"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.other_owners.all()


class IsClassMemberPermission(BasePermission):
    message = "you are not a member of the class"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.enrolled.all()
