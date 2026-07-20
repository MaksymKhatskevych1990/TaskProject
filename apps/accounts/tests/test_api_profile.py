"""Profile API tests."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory

User = get_user_model()


class ProfileAPITests(BaseAPITestCase):
    """Verify self-service profile endpoints."""

    def test_me_endpoint_returns_profile(self) -> None:
        """Authenticated users can read their own profile."""
        user = UserFactory(
            email="me@example.com",
            first_name="Me",
            last_name="User",
            password="StrongPass123!",
        )
        user.profile.position = "Engineer"
        user.profile.save()
        self.authenticate(user)

        response = self.client.get(reverse("api:v1:accounts:me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["email"], "me@example.com")
        self.assertEqual(response.data["data"]["profile"]["position"], "Engineer")

    def test_me_endpoint_updates_profile(self) -> None:
        """Authenticated users can update their own profile."""
        user = UserFactory(password="StrongPass123!")
        self.authenticate(user)

        response = self.client.patch(
            reverse("api:v1:accounts:me"),
            {"first_name": "Updated", "position": "Lead"},
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.profile.position, "Lead")

    def test_me_password_endpoint_changes_password(self) -> None:
        """Authenticated users can change their password."""
        user = UserFactory(password="OldPass123!")
        self.authenticate(user)

        response = self.client.post(
            reverse("api:v1:accounts:me-password"),
            {
                "current_password": "OldPass123!",
                "new_password": "NewPass123!",
            },
            format="json",
        )

        user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password("NewPass123!"))
