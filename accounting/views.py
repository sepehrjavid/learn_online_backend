from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from accounting.models import CustomUser
from accounting.serializers import UserSerializer


class UserSignUpAPIView(APIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = self.request.data.get("password")
        token_serializer = JSONWebTokenSerializer(data={"username": user.username, "password": password})
        token_serializer.is_valid(raise_exception=True)
        res = {
            "token": token_serializer.validated_data.get("token"),
        }
        return Response(res, status=status.HTTP_201_CREATED)


class GetUserDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
