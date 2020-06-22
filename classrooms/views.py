from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView,
                                     GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classrooms.models import Classroom
from classrooms.permissions import IsClassroomCreatorPermission, IsClassroomOwnerPermission
from classrooms.serializers import (ClassroomCreateSerializer, ClassroomEditSerializer, ClassroomBriefSerializer,
                                    AddOwnerToClassSerializer)


class ListClassAPIView(ListAPIView):
    queryset = Classroom.objects.filter(is_active=True)
    serializer_class = ClassroomBriefSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        qs = Classroom.objects.filter(is_active=True)
        if query:
            qs = qs.filter(Q(name__icontains=query) |
                           Q(description__icontains=query) |
                           Q(creator__first_name__contains=query) |
                           Q(creator__last_name__contains=query))
        return qs


class RetrieveClassAPIView(RetrieveAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomBriefSerializer


class UpdateClassAPIView(UpdateAPIView):
    queryset = Classroom.objects.all()
    permission_classes = [IsClassroomCreatorPermission]
    serializer_class = ClassroomEditSerializer


class CreateClassAPIView(CreateAPIView):
    queryset = Classroom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DeactivateClassAPIView(DestroyAPIView):
    queryset = Classroom.objects.all()
    permission_classes = [IsClassroomCreatorPermission]

    def delete(self, request, *args, **kwargs):
        classroom = self.get_object()
        classroom.is_active = False
        classroom.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddOwnerToClassAPIView(GenericAPIView):
    permission_classes = [IsClassroomCreatorPermission]
    serializer_class = AddOwnerToClassSerializer
    queryset = Classroom.objects.all()

    def put(self, request, pk):
        classroom = self.get_object()
        ser = self.serializer_class(data=request.data, context={"request": self.request})
        ser.is_valid(raise_exception=True)
        classroom.other_owners.set(ser.validated_data.get("other_owners"))
        return Response(ClassroomBriefSerializer(classroom).data, status=status.HTTP_200_OK)


class ToggleEnrollClassAPIView(APIView):
    def get(self, request, pk):
        classroom = get_object_or_404(Classroom, id=pk)
        if request.user in classroom.enrolled.all():
            classroom.enrolled.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            if request.user == classroom.creator or request.user in classroom.other_owners.all():
                return Response("Creator or Owner of a class cannot enroll")
            classroom.enrolled.add(request.user)
            return Response(ClassroomBriefSerializer(classroom).data, status=status.HTTP_200_OK)


class QuitClassOwnershipAPIView(GenericAPIView):
    permission_classes = [IsClassroomOwnerPermission]
    queryset = Classroom.objects.all()

    def delete(self, request, pk):
        classroom = self.get_object()
        classroom.other_owners.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
