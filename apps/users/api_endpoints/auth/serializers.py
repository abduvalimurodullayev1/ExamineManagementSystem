from rest_framework import serializers
from apps.users.models import User

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

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User(email=email, password=password)
        return user
