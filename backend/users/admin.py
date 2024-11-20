from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ("id", "username", "email", "is_verified")
    readonly_fields = ("last_login",)
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "password",
                    "username",
                    "email",
                    "profile_picture",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "profile_picture",
                    "is_verified",
                    "password1",
                    "password2",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("username",)
