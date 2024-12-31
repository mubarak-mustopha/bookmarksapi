from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .views import (
    RegisterUserAPIView,
    UsernameLoginAPIView,
    EmailLoginAPIView,
    LogoutAPIView,
)


urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register-user"),
    path("username_login/", UsernameLoginAPIView.as_view(), name="username-login"),
    path("email_login/", EmailLoginAPIView.as_view(), name="email-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
