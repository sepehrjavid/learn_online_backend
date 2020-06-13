from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from accounting.models import CustomUser
from accounting.serializers import UserSerializer, UserEditSerializer, UserListSerializer, ChangePasswordSerializer


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


class EditUserAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user


class GetUserListAPIView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        qs = CustomUser.objects.all()
        if query:
            qs = qs.filter(email__icontains=query)
        return qs


class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(serializer.validated_data.get("current_password")):
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)
