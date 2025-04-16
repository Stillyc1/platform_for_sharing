from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from users.forms import LoginUserForm, CustomUserCreationForm
from users.services import UserIsNotAuthenticated


class LoginUserView(UserIsNotAuthenticated, LoginView):
    """Авторизация через веб-интерфейс."""
    template_name = 'users/login.html'
    form_class = LoginUserForm


class RegisterView(UserIsNotAuthenticated, CreateView):
    """Регистрация через веб-интерфейс."""
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('platform_for_sharing:home')
