"""Authentication API tests."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.base import BaseAPITestCase
from tests.factories.accounts import UserFactory

User = get_user_model()


class AuthAPITests(BaseAPITestCase):
    """Verify JWT authentication endpoints."""

    def test_obtain_token_with_email(self) -> None:
        """Users can obtain tokens using their email address."""
        UserFactory(email="auth@example.com", password="StrongPass123!")

        response = self.client.post(
            reverse("api:v1:token-obtain"),
            {"email": "auth@example.com", "password": "StrongPass123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "auth@example.com")

    def test_refresh_token(self) -> None:
        """Refresh tokens issue a new access token."""
        UserFactory(email="refresh@example.com", password="StrongPass123!")
        token_response = self.client.post(
            reverse("api:v1:token-obtain"),
            {"email": "refresh@example.com", "password": "StrongPass123!"},
            format="json",
        )

        response = self.client.post(
            reverse("api:v1:token-refresh"),
            {"refresh": token_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout_blacklists_refresh_token(self) -> None:
        """Logout invalidates the submitted refresh token."""
        user = UserFactory(email="logout@example.com", password="StrongPass123!")
        token_response = self.client.post(
            reverse("api:v1:token-obtain"),
            {"email": "logout@example.com", "password": "StrongPass123!"},
            format="json",
        )
        self.authenticate(user)

        logout_response = self.client.post(
            reverse("api:v1:token-logout"),
            {"refresh": token_response.data["refresh"]},
            format="json",
        )
        refresh_response = self.client.post(
            reverse("api:v1:token-refresh"),
            {"refresh": token_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
