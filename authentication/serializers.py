from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, **kwargs):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]

        user = User.objects.create_user(username, email, password)
        return user


class UsernameLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(username=username, password=password)

        if user is None or not user.is_active:
            raise AuthenticationFailed(
                "No active account found for the provided crendentials"
            )

        return {
            "username": user.username,
            "email": user.email,
            "tokens": user.tokens,
        }


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(email=email, password=password)

        if user is None or not user.is_active:
            raise AuthenticationFailed(
                "No active account found for the provided crendentials"
            )

        return {
            "username": user.username,
            "email": user.email,
            "tokens": user.tokens,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token = attrs["refresh"]

        try:
            RefreshToken(token).blacklist()
        except Exception as e:
            import pdb

            pdb.set_trace()
            raise serializers.ValidationError(e.args[0])

        return {}
