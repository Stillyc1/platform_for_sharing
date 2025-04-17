from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.forms import CustomUserCreationForm, LoginUserForm
from users.models import User
from users.serializers import UserSerializer
from users.services import UserIsNotAuthenticated


class LoginUserView(UserIsNotAuthenticated, LoginView):
    """Авторизация через веб-интерфейс."""

    template_name = "users/login.html"
    form_class = LoginUserForm


class RegisterView(UserIsNotAuthenticated, CreateView):
    """Регистрация через веб-интерфейс."""

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("platform_for_sharing:home")


class UserCreateAPIView(CreateAPIView):
    """Реализация представления регистрации пользователя, через CreateAPIView."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Хэшируем пароль при создании пользователя."""
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Реализация представления просмотра пользователя, через RetrieveAPIView."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
