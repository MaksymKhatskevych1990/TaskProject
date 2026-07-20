"""Account model tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.choices import UserRole
from apps.accounts.models import Profile
from tests.factories.accounts import UserFactory

User = get_user_model()


class UserModelTests(TestCase):
    """Verify user model behavior."""

    def test_user_is_created_with_profile(self) -> None:
        """A profile is created automatically for every user."""
        user = UserFactory(email="member@example.com")

        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.email, "member@example.com")

    def test_role_capabilities(self) -> None:
        """Role helpers expose the expected capabilities."""
        admin = UserFactory(role=UserRole.ADMIN)
        manager = UserFactory(role=UserRole.MANAGER)
        employee = UserFactory(role=UserRole.EMPLOYEE)

        self.assertTrue(admin.is_admin)
        self.assertTrue(admin.is_manager)
        self.assertTrue(manager.is_manager)
        self.assertFalse(manager.is_admin)
        self.assertTrue(employee.is_employee)
        self.assertFalse(employee.is_manager)
