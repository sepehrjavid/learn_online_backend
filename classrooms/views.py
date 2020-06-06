from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from classrooms.models import Classroom


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
