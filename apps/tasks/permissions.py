"""Task-specific API permissions."""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class CanManageTasks(BasePermission):
    """Allow managers and administrators to manage tasks."""

    message = "Only managers can manage tasks."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check whether the requester can manage tasks."""
        user = request.user
        return bool(user and user.is_authenticated and user.is_manager)
