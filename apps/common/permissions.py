"""Small reusable DRF permission helpers."""

from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


def _authenticated_user(request: Request) -> bool:
    """Return whether the request has an authenticated user."""
    return bool(request.user and request.user.is_authenticated)


def _user_flag(request: Request, attribute: str) -> bool:
    """Read a boolean role capability without coupling to a user model."""
    if not _authenticated_user(request):
        return False
    value = getattr(request.user, attribute, False)
    return bool(value() if callable(value) else value)


class IsAdmin(BasePermission):
    """Allow authenticated staff or superusers."""

    message = "Administrator access is required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check Django's built-in administrative flags."""
        return _authenticated_user(request) and bool(
            request.user.is_staff or request.user.is_superuser
        )


class IsManager(BasePermission):
    """Allow users exposing a true ``is_manager`` capability."""

    message = "Manager access is required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check the user capability without defining project RBAC."""
        return _user_flag(request, "is_manager")


class IsEmployee(BasePermission):
    """Allow users exposing a true ``is_employee`` capability."""

    message = "Employee access is required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check the user capability without defining project RBAC."""
        return _user_flag(request, "is_employee")


class IsOwner(BasePermission):
    """Allow access when the object belongs to the requesting user."""

    message = "You do not own this resource."

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Any,
    ) -> bool:
        """Compare the user with the view's configured owner field."""
        owner_field = getattr(view, "owner_field", "created_by")
        owner = obj if obj == request.user else getattr(obj, owner_field, None)
        return _authenticated_user(request) and owner == request.user


class IsAuthenticated(BasePermission):
    """Allow authenticated users."""

    message = "Authentication credentials were not provided."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check request authentication."""
        return _authenticated_user(request)


class IsAnonymous(BasePermission):
    """Allow only unauthenticated requests."""

    message = "This endpoint is available only to anonymous users."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Reject authenticated users."""
        return not _authenticated_user(request)
