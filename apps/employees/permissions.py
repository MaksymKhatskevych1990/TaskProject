"""Employees domain permissions."""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class CanManageOrganization(BasePermission):
    """Allow managers and administrators to manage org structure."""

    message = "Manager access is required to manage employees, teams, or positions."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check the authenticated user's manager capability."""
        user = request.user
        return bool(user and user.is_authenticated and user.is_manager)
