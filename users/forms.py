from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ваш логин"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите логин"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-select"})
        self.fields["password2"].widget.attrs.update({"class": "form-select"})

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )
