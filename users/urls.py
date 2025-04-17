from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from users.apps import UsersConfig
from users.views import RegisterView, LoginUserView, UserCreateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register_api/', UserCreateAPIView.as_view(), name='register_api'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user'),
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
