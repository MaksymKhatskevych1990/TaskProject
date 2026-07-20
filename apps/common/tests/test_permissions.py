"""Tests for reusable permission helpers."""

from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from rest_framework.views import APIView

from apps.common.permissions import (
    IsAdmin,
    IsAnonymous,
    IsAuthenticated,
    IsEmployee,
    IsManager,
    IsOwner,
)


class PermissionTests(SimpleTestCase):
    """Verify permissions without defining project RBAC."""

    view = APIView()

    def test_authentication_permissions_are_complementary(self) -> None:
        """Authenticated and anonymous helpers make opposite decisions."""
        authenticated = SimpleNamespace(is_authenticated=True)
        authenticated_request = SimpleNamespace(user=authenticated)
        anonymous_request = SimpleNamespace(user=AnonymousUser())

        self.assertTrue(
            IsAuthenticated().has_permission(authenticated_request, self.view)
        )
        self.assertFalse(
            IsAnonymous().has_permission(authenticated_request, self.view)
        )
        self.assertFalse(IsAuthenticated().has_permission(anonymous_request, self.view))
        self.assertTrue(IsAnonymous().has_permission(anonymous_request, self.view))

    def test_admin_permission_uses_django_admin_flags(self) -> None:
        """Staff and superusers receive administrative access."""
        user = SimpleNamespace(
            is_authenticated=True,
            is_staff=True,
            is_superuser=False,
        )

        self.assertTrue(
            IsAdmin().has_permission(SimpleNamespace(user=user), self.view)
        )

    def test_role_permissions_use_user_capabilities(self) -> None:
        """Manager and employee checks remain independent of a role model."""
        user = SimpleNamespace(
            is_authenticated=True,
            is_manager=lambda: True,
            is_employee=False,
        )
        request = SimpleNamespace(user=user)

        self.assertTrue(IsManager().has_permission(request, self.view))
        self.assertFalse(IsEmployee().has_permission(request, self.view))

    def test_owner_permission_uses_configurable_field(self) -> None:
        """Views can identify the relevant ownership attribute."""
        user = SimpleNamespace(is_authenticated=True)
        request = SimpleNamespace(user=user)
        resource = SimpleNamespace(assignee=user)
        view = SimpleNamespace(owner_field="assignee")

        self.assertTrue(
            IsOwner().has_object_permission(request, view, resource)
        )
