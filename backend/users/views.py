import hashlib
import logging
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from requests.models import HTTPBasicAuth
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
from collections import defaultdict
from functools import reduce
from operator import or_

import requests
from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import redirect, render
from django.utils import timezone
from requests.models import HTTPBasicAuth
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from backend.users.models import PasswordResetToken, RecentAction, User, VerificationCode
from backend.users.serializers import (
    UserChangePasswordSerializer,
    UserForgotPasswordSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserResetPasswordSerializer,
    UserSerializer,
)

# Template views
def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')

def verify_view(request):
    return render(request, 'auth/verify.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')



@method_decorator(csrf_exempt, name='dispatch')
class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        new_email = request.data.get("email", None)
        if new_email and new_email != user.email:
            logging.warning(f"User {user.id} attempted to change email from {user.email} to {new_email}")
            return Response(
                {"message": "Email change is not allowed. Please contact support."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        name = serializer.validated_data.get("name")
        password = serializer.validated_data.get("password")

        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create user (will be inactive until verified)
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password
            )
            
            # Create and send verification code
            verification_code = VerificationCode.objects.create(user=user)
            
            try:
                verification_code.send()
                if settings.DEBUG:
                    message = f"User created successfully. Verification code: {verification_code.code} (Check email or console)"
                else:
                    message = "User created successfully. Please check your email for verification code."
            except Exception as email_error:
                logging.error(f"Email sending failed: {email_error}")
                message = f"User created successfully. Verification code: {verification_code.code} (Email sending failed)"
            
            return Response(
                {"message": message},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logging.error(f"User creation failed: {e}")
            return Response(
                {"message": f"Error creating user: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            data = {"message": "Email address is not valid."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=request.data["email"])
            if not user.is_active:
                return Response(data={"message": "Account is inactive."}, status=status.HTTP_403_FORBIDDEN)

            if user.check_password(request.data["password"]):
                from rest_framework.authtoken.models import Token

                token, created = Token.objects.get_or_create(user=user)
                return Response(data={"token": token.key}, status=status.HTTP_200_OK)
            return Response(
                data={"message": "Email or password is wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except User.DoesNotExist:
            return Response(
                data={"message": "Email or password is wrong."},
                status=status.HTTP_404_NOT_FOUND,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(data={"message": "User logged out."}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data)
        user = self.request.user
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("current_password")):
                return Response({"message": "Current password is wrong."}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get("current_password") == serializer.data.get("new_password"):
                return Response(
                    {"message": "New password must be different from the current password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                validate_password(serializer.data.get("new_password"), user)
            except ValidationError:
                return Response(
                    {
                        "message": "This password is too short (must be at least 8 characters), "
                        "too common, or entirely numeric. Please choose a stronger password."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserVerifyAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", None)
        if not code:
            return Response(
                {"message": "Verification code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.data.get("email", None)
        if not email:
            return Response(
                {"message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            verification_code = VerificationCode.objects.get(code=code, user__email=email)
            if verification_code.is_expired:
                return Response(
                    {"message": "Verification code has expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            verification_code.user.is_active = True
            verification_code.user.save()
            verification_code.delete()
            return Response(
                {"message": "Account activated successfully."},
                status=status.HTTP_200_OK,
            )
        except VerificationCode.DoesNotExist:
            return Response(
                {"message": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserResendVerificationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        if not email:
            return Response(
                {"message": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            # Delete any existing verification codes for this user
            VerificationCode.objects.filter(user=user).delete()
            # Create and send new verification code
            verification_code = VerificationCode.objects.create(user=user)
            verification_code.send()
            return Response(
                {"message": "Verification code sent successfully."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            # Return success to prevent email enumeration
            return Response(
                {"message": "Verification code sent successfully."},
                status=status.HTTP_200_OK,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            # Delete any existing tokens for this user
            PasswordResetToken.objects.filter(user=user).delete()
            # Create a new token
            reset_token = PasswordResetToken.objects.create(user=user)
            reset_token.send()
            return Response(
                {"message": "Password reset instructions were sent successfully."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            # Return the exact same message to prevent email enumeration attacks
            return Response(
                {"message": "Password reset instructions were sent successfully."},
                status=status.HTTP_200_OK,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = PasswordResetToken.objects.select_for_update().get(token=serializer.validated_data["token"])
            if reset_token.is_expired:
                return Response(
                    {"message": "Password reset link has expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = reset_token.user

            # Check if the new password is the same as the old password
            if user.check_password(serializer.validated_data["new_password"]):
                return Response(
                    {"message": "New password must be different from your current password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                validate_password(serializer.validated_data["new_password"], user)
            except ValidationError:
                return Response(
                    {
                        "message": "This password is too short (must be at least 8 characters), "
                        "too common, or entirely numeric. Please choose a stronger password."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            reset_token.delete()
            return Response(
                {"message": "Password reset successfully."},
                status=status.HTTP_200_OK,
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"message": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"message": "Something went wrong."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name='dispatch')
class UserResetPasswordValidateAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token", None)
        if not token:
            return Response(
                {"message": "Token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_expired:
                return Response(
                    {"message": "Password reset link has expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"message": "Token is valid."},
                status=status.HTTP_200_OK,
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"message": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
