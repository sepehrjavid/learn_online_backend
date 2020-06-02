from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from accounting.views import UserSignUpAPIView

app_name = "accounting"

urlpatterns = [
    path('login', obtain_jwt_token),
    path('verify', verify_jwt_token),
    path('signup', UserSignUpAPIView.as_view())
]
