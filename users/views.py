from django.contrib.auth.views import LoginView as LoginViewContrib
from django.contrib.auth.views import LogoutView as LogoutViewContrib
from django.views.generic import CreateView

from users.forms import CustomAuthForm, RegisterForm
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = "/"


class LoginView(LoginViewContrib):
    form_class = CustomAuthForm
    template_name = "users/login.html"
    success_url = "/"


class LogoutView(LogoutViewContrib):
    pass
