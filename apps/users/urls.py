from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.i18n import set_language
from django.contrib.auth import views as auth_views

from users.views import *

app_name = "users"
# urlpatterns = [
#     path("register/", RegisterApiView.as_view(), name='register'),
#     path("register-verify/", VerifyEmailView.as_view(), name='register-verify'),
#     path("login/", LoginAPIView.as_view()),
#     # path('verify-register-email/', VerifyRegisterEmailView.as_view(), name='verify-register-email'),
#     path('verify-forgot-email/', VerifyForgotEmailView.as_view(), name='verify-register-email'),
#     path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
#     path('change-password/', ChangePasswordView.as_view(), name='change_password'),
#
# ]
