from rest_framework import serializers
from cloudinary.templatetags import cloudinary

from backend.common.serializers import UUIDModelSerializer
from backend.users.models import User


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "email", "name", "is_staff", "is_active", "grade", "track", "profile_completed", "date_joined", "profile_picture")
        read_only_fields = ("id", "email", "is_staff", "is_active", "profile_completed", "date_joined")
    
    def get_profile_picture(self, obj):
        """Return the full Cloudinary URL for the profile picture"""
        if obj.profile_picture:
            # Use Cloudinary's build_url to get the full URL
            return obj.profile_picture.url
        return None
    
    def validate(self, attrs):
        # Validate that if grade > 8, track must be provided and not 'lgs'
        grade = attrs.get('grade')
        track = attrs.get('track')
        
        # If grade is not being updated, use the existing value
        if grade is None and self.instance:
            grade = self.instance.grade
        
        # If track is not being updated, use the existing value
        if track is None and self.instance:
            track = self.instance.track
        
        if grade and grade > 8:
            if not track or track == 'lgs':
                raise serializers.ValidationError({
                    "track": "9. sınıf ve üzeri için Sayısal veya Sözel alan seçmelisiniz."
                })
        
        # If grade <= 8, track should be 'lgs'
        if grade and grade <= 8:
            if track and track != 'lgs':
                raise serializers.ValidationError({
                    "track": "8. sınıf ve altı için sadece LGS seçeneği geçerlidir."
                })
            # Auto-set to lgs if not provided
            if 'grade' in attrs:  # Only auto-set if grade is being updated
                attrs['track'] = 'lgs'
        
        return attrs


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
        fields = ("email", "name", "password", "grade", "track")
    
    def validate(self, attrs):
        # Validate that if grade > 8, track must be provided and not 'lgs'
        grade = attrs.get('grade')
        track = attrs.get('track')
        
        if grade and grade > 8:
            if not track or track == 'lgs':
                raise serializers.ValidationError({
                    "track": "9. sınıf ve üzeri için Sayısal veya Sözel alan seçmelisiniz."
                })
        
        # If grade <= 8, track should be 'lgs'
        if grade and grade <= 8:
            if track and track != 'lgs':
                raise serializers.ValidationError({
                    "track": "8. sınıf ve altı için sadece LGS seçeneği geçerlidir."
                })
            # Auto-set to lgs if not provided
            attrs['track'] = 'lgs'
        
        return attrs


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


class UserCompleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("grade", "track")
    
    def validate(self, attrs):
        grade = attrs.get('grade')
        track = attrs.get('track')
        
        if not grade:
            raise serializers.ValidationError({
                "grade": "Sınıf bilgisi zorunludur."
            })
        
        if not track:
            raise serializers.ValidationError({
                "track": "Alan bilgisi zorunludur."
            })
        
        # Validate that if grade > 8, track must not be 'lgs'
        if grade > 8:
            if track == 'lgs':
                raise serializers.ValidationError({
                    "track": "9. sınıf ve üzeri için Sayısal veya Sözel alan seçmelisiniz."
                })
        
        # If grade <= 8, track should be 'lgs'
        if grade <= 8:
            if track != 'lgs':
                raise serializers.ValidationError({
                    "track": "8. sınıf ve altı için sadece LGS seçeneği geçerlidir."
                })
        
        return attrs
