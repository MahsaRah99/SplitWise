from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from .models import User
from .utils import send_verification_email


def email_validator(value):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (email_validator,)},
        }

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            send_verification_email(user)
            return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if user:
                data["user"] = user
                return data
            else:
                raise serializers.ValidationError("Invalid Usrename or Password.")
        raise serializers.ValidationError("Email and password are required.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "profile_picture")
        read_only_fields = ("email",)


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_new_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("current_password", "new_password", "confirm_new_password")

    def validate_current_password(self, value):
        user = self.context.get("user")
        if not user.check_password(value):
            raise serializers.ValidationError("Wrong password")
        return value

    def validate(self, data):
        new_password = data.get("new_password")
        confirm_new_password = data.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords should match!")
        return data

    def save(self, **kwargs):
        user = self.context.get("user")
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user
