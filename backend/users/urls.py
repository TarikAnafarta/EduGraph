from django.urls import path

from backend.users.views import (
    UserAPIView,
    UserLoginAPIView,
    UserRegisterAPIView,
    UserLogoutAPIView,
    UserChangePasswordAPIView,
    UserVerifyAPIView,
    UserResendVerificationAPIView,
    UserForgotPasswordAPIView,
    UserResetPasswordAPIView,
    UserResetPasswordValidateAPIView,
)

app_name = "users"

urlpatterns = [
    # API endpoints
    path("me/", UserAPIView.as_view(), name="user-me"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("change-password/", UserChangePasswordAPIView.as_view(), name="user-change-password"),
    path("verify/", UserVerifyAPIView.as_view(), name="user-verify"),
    path("resend-verification/", UserResendVerificationAPIView.as_view(), name="user-resend-verification"),
    path("forgot-password/", UserForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", UserResetPasswordAPIView.as_view(), name="reset-password"),
    path("reset-password/validate/", UserResetPasswordValidateAPIView.as_view(), name="reset-password-validate"),
]
