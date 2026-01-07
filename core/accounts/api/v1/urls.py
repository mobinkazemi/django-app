from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api-v1"


urlpatterns = [
    # Registration api
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    # Basic token api
    path("token/login/", views.CustomAuthTokenView.as_view(), name="token-login"),
    path("token/logout/", views.CustomAuthLogoutView.as_view(), name="token-logout"),
    # JWT token api
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # Password api
    path(
        "password/reset/", views.ResetPasswordAPIView.as_view(), name="reset-password"
    ),
]
