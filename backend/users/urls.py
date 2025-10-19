from django.urls import path

from backend.users import views
from backend.users.views import (
    UserForgotPasswordAPIView,
    UserResetPasswordAPIView,
    UserResetPasswordValidateAPIView,
    login_view,
    register_view,
    verify_view,
)

app_name = "users"

urlpatterns = [
    # API endpoints
    path("me/", view=views.UserAPIView.as_view(), name="user-me"),
    path("login/", view=views.UserLoginAPIView.as_view(), name="user-login"),
    path("register/", view=views.UserRegisterAPIView.as_view(), name="user-register"),
    path("logout/", view=views.UserLogoutAPIView.as_view(), name="user-logout"),
    path("change-password/", view=views.UserChangePasswordAPIView.as_view(), name="user-change-password"),
    path("verify/", view=views.UserVerifyAPIView.as_view(), name="user-verify"),
    path("resend-verification/", view=views.UserResendVerificationAPIView.as_view(), name="user-resend-verification"),
    path("forgot-password/", UserForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", UserResetPasswordAPIView.as_view(), name="reset-password"),
    path("reset-password/validate/", UserResetPasswordValidateAPIView.as_view(), name="reset-password-validate"),
]
