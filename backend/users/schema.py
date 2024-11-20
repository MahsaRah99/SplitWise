from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status

from .serializers import UserRegisterSerializer

user_register_schema = extend_schema(
    summary="Register a new user",
    description="Registers a new user with a username, email, and optional profile picture.",
    request=UserRegisterSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            "Success Response",
            examples=[
                OpenApiExample(
                    "Example 1",
                    value={
                        "username": "john doe",
                        "email": "johndoe@example.com",
                        "profile_picture": "http://example.com/media/profile_pics/johndoe.jpg",
                    },
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            "Error Response",
            examples=[
                OpenApiExample(
                    "Example 2",
                    value={
                        "detail": "Validation error occurred. Email already exists."
                    },
                ),
            ],
        ),
    },
)
