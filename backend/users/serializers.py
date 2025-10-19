from rest_framework import serializers

from backend.common.serializers import UUIDModelSerializer
from backend.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "is_staff", "is_active")


class UserDetailSerializer(UUIDModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name")


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name")


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "password")


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"message": "Passwords do not match."})
        return attrs


class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"message": "Passwords do not match."})
        return attrs
