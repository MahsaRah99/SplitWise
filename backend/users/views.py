import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsProfileOwner, IsVerified
from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "A Verification Email Was Sent to You."},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            return Response(
                {"detail": "Email verified successfully."}, status=status.HTTP_200_OK
            )
        except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            User.DoesNotExist,
        ):
            return Response(
                {"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        srz_data = self.get_serializer(data=request.data)
        srz_data.is_valid(raise_exception=True)

        user = srz_data.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request == "GET":
            permission_classes = [IsVerified]
        else:
            permission_classes = [IsProfileOwner]
        return [permission() for permission in permission_classes]


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsVerified]

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password Changed Successfuly"},
            status=status.HTTP_200_OK,
        )
