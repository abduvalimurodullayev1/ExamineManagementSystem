from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.i18n import set_language
from django.contrib.auth import views as auth_views

from apps.users.api_endpoints.auth.views import LoginView, RegisterView, ResetPasswordView
app_name = "users"

urlpatterns = [
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
