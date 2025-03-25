from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class VerificationEmailSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'verification_code']
        extra_kwargs = {"password": {"write_only": True}}


class ForgotChangeUserModelSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'new_password', 'confirm_password', 'verification_code']
        extra_kwargs = {"new_password": {"write_only": True},
                        "confirm_password": {"write_only": True},
                        "verification_code": {"write_only": True}}


class ChangeUserModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=55)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True},
                        'confirm_password': {'write_only': True}}


class ForgotPasswordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        attrs["user"] = user
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"uid": "Invalid user ID"})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        attrs["user"] = user
        return attrs
