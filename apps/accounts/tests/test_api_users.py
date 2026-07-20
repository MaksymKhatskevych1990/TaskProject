"""Administrative user API tests."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.accounts.choices import UserRole
from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory

User = get_user_model()


class UserManagementAPITests(BaseAPITestCase):
    """Verify administrative user management endpoints."""

    def test_admin_can_create_user(self) -> None:
        """Administrators can create new users."""
        admin = UserFactory(role=UserRole.ADMIN, password="AdminPass123!")
        self.authenticate(admin)

        response = self.client.post(
            reverse("api:v1:accounts:user-list"),
            {
                "email": "created@example.com",
                "password": "StrongPass123!",
                "first_name": "Created",
                "last_name": "User",
                "role": UserRole.EMPLOYEE,
                "position": "Designer",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="created@example.com").exists())
        self.assertEqual(
            User.objects.get(email="created@example.com").profile.position,
            "Designer",
        )

    def test_admin_can_create_user_with_telegram(self) -> None:
        """Administrators can attach Telegram data when creating users."""
        admin = UserFactory(role=UserRole.ADMIN, password="AdminPass123!")
        self.authenticate(admin)

        response = self.client.post(
            reverse("api:v1:accounts:user-list"),
            {
                "email": "telegram@example.com",
                "password": "StrongPass123!",
                "first_name": "Telegram",
                "last_name": "User",
                "role": UserRole.EMPLOYEE,
                "telegram_username": "@worker_bot",
                "telegram_chat_id": 123456789,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = User.objects.get(email="telegram@example.com").telegram_account
        self.assertEqual(account.username, "worker_bot")
        self.assertEqual(account.chat_id, 123456789)

    def test_employee_cannot_create_user(self) -> None:
        """Non-administrators cannot create users."""
        employee = UserFactory(role=UserRole.EMPLOYEE)
        self.authenticate(employee)

        response = self.client.post(
            reverse("api:v1:accounts:user-list"),
            {
                "email": "blocked@example.com",
                "password": "StrongPass123!",
                "first_name": "Blocked",
                "last_name": "User",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_deactivate_user(self) -> None:
        """Administrators can deactivate another user."""
        admin = UserFactory(role=UserRole.ADMIN)
        target = UserFactory(email="target@example.com")
        self.authenticate(admin)

        response = self.client.delete(
            reverse("api:v1:accounts:user-detail", kwargs={"uuid": target.uuid})
        )

        target.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(target.is_active)
