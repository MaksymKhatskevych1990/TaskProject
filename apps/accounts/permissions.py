"""Account-specific API permissions."""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.accounts.choices import UserRole


class CanManageUsers(BasePermission):
    """Allow administrators to manage other user accounts."""

    message = "Only administrators can manage users."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check whether the requester is an administrator."""
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role == UserRole.ADMIN)
        )
