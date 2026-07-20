"""Telegram admin tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.choices import UserRole
from apps.telegram.models import TelegramAccount

User = get_user_model()


class TelegramAccountAdminTests(TestCase):
    """Verify admin user creation does not duplicate Telegram accounts."""

    def test_add_user_via_admin_updates_existing_telegram_account(self) -> None:
        """Creating a user with Telegram inline data should not violate uniqueness."""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPass123!",
            first_name="Admin",
            last_name="User",
        )
        self.client.force_login(admin_user)

        response = self.client.post(
            reverse("admin:accounts_user_add"),
            {
                "email": "employee@example.com",
                "first_name": "Employee",
                "last_name": "User",
                "role": UserRole.EMPLOYEE,
                "password1": "EmployeePass123!",
                "password2": "EmployeePass123!",
                "is_active": "on",
                "profile-TOTAL_FORMS": "1",
                "profile-INITIAL_FORMS": "0",
                "profile-MIN_NUM_FORMS": "0",
                "profile-MAX_NUM_FORMS": "1",
                "profile-0-phone": "",
                "profile-0-position": "",
                "profile-0-bio": "",
                "profile-0-timezone": "Europe/Kyiv",
                "telegram_account-TOTAL_FORMS": "1",
                "telegram_account-INITIAL_FORMS": "0",
                "telegram_account-MIN_NUM_FORMS": "1",
                "telegram_account-MAX_NUM_FORMS": "1",
                "telegram_account-0-username": "worker",
                "telegram_account-0-chat_id": "123456789",
                "telegram_account-0-notifications_enabled": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="employee@example.com")
        self.assertEqual(TelegramAccount.objects.filter(user=user).count(), 1)
        account = user.telegram_account
        self.assertEqual(account.username, "worker")
        self.assertEqual(account.chat_id, 123456789)
