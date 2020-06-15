from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classrooms.models import Classroom
from classrooms.permissions import ClassroomIsOwnerPermission
from classrooms.serializers import (ClassroomSerializer, ClassroomEditSerializer, ClassroomBriefSerializer,
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
    permission_classes = [ClassroomIsOwnerPermission]
    serializer_class = ClassroomEditSerializer


class CreateClassAPIView(CreateAPIView):
    queryset = Classroom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DeactivateClassAPIView(APIView):
    def delete(self, request, pk):
        classroom = get_object_or_404(Classroom, id=pk)
        if classroom.creator != request.user:
            return Response({
                "detail": "You do not have permission to perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
        classroom.is_active = False
        classroom.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddOwnerToClassAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddOwnerToClassSerializer

    def put(self, request, pk):
        classroom = get_object_or_404(Classroom, id=pk)
        if classroom.creator != request.user:
            return Response({
                "detail": "You do not have permission to perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
        ser = self.serializer_class(data=request.data, context={"request": self.request})
        ser.is_valid(raise_exception=True)
        classroom.other_owners.set(ser.validated_data.get("owners"))
        return Response(status=status.HTTP_204_NO_CONTENT)
