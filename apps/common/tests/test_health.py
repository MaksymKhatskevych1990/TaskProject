"""Tests for infrastructure health endpoints."""

from django.test import TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    """Verify that orchestration health checks are available anonymously."""

    def test_liveness_endpoint(self) -> None:
        """Liveness returns success without authentication."""
        response = self.client.get(reverse("health:liveness"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_readiness_endpoint(self) -> None:
        """Readiness verifies the configured database and cache."""
        response = self.client.get(reverse("health:readiness"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["checks"]["database"], "ok")
        self.assertEqual(response.json()["checks"]["cache"], "ok")
