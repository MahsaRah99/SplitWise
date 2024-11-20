from rest_framework.permissions import BasePermission


class PrimaryPermission(BasePermission):
    message = "Not Authenticated"

    def additional_permission(self, request, view) -> bool:
        return True

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and self.additional_permission(request, view)
        )


class IsVerified(PrimaryPermission):
    message = "Email Not Verified"

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_verified


class IsProfileOwner(IsVerified):
    message = "You are not allowed this profile"

    def has_object_permission(self, request, view, obj):
        return obj == request.user
