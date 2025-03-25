from django.contrib.auth.hashers import make_password
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
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
