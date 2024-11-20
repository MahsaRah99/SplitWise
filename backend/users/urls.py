from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("auth/register/", views.UserRegisterView.as_view(), name="user_register"),
    path(
        "auth/verify-email/<str:token>/",
        views.VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path("auth/login/", views.UserLoginView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path(
        "password/change/", views.ChangePasswordView.as_view(), name="change_password"
    ),
]
