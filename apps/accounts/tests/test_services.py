"""Account service tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.accounts import services
from apps.accounts.choices import UserRole
from tests.factories.accounts import UserFactory

User = get_user_model()


class AccountServiceTests(TestCase):
    """Verify account write operations."""

    def test_create_user_creates_profile(self) -> None:
        """Creating a user also stores profile data."""
        admin = UserFactory(role=UserRole.ADMIN)
        user = services.create_user(
            email="new.user@example.com",
            password="StrongPass123!",
            first_name="New",
            last_name="User",
            role=UserRole.EMPLOYEE,
            actor=admin,
            profile_data={"position": "Developer", "timezone": "Europe/Berlin"},
        )

        self.assertEqual(user.profile.position, "Developer")
        self.assertEqual(user.profile.timezone, "Europe/Berlin")
        self.assertEqual(user.profile.created_by, admin)

    def test_create_user_rejects_duplicate_email(self) -> None:
        """Duplicate emails are rejected."""
        UserFactory(email="duplicate@example.com")

        with self.assertRaises(ValidationError):
            services.create_user(
                email="duplicate@example.com",
                password="StrongPass123!",
                first_name="Dup",
                last_name="User",
            )

    def test_change_password_validates_current_password(self) -> None:
        """Password changes require the current password."""
        user = UserFactory(password="OldPass123!")

        with self.assertRaises(ValidationError):
            services.change_password(
                user=user,
                current_password="wrong-password",
                new_password="NewPass123!",
            )

        services.change_password(
            user=user,
            current_password="OldPass123!",
            new_password="NewPass123!",
        )
        user.refresh_from_db()
        self.assertTrue(user.check_password("NewPass123!"))
