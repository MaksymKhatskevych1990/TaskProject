"""Reusable test cases."""

from typing import Any

from django.core.cache import caches
from django.test import TestCase
from rest_framework.test import APITestCase


class CacheIsolationMixin:
    """Clear every configured cache before each test."""

    def setUp(self) -> None:
        """Reset cache state."""
        super().setUp()  # type: ignore[misc]
        for cache in caches.all():
            cache.clear()


class BaseTestCase(CacheIsolationMixin, TestCase):
    """Base class for project unit and integration tests."""


class BaseAPITestCase(CacheIsolationMixin, APITestCase):
    """Base class for authenticated API tests."""

    def authenticate(self, user: Any) -> None:
        """Authenticate subsequent requests as the supplied user."""
        self.client.force_authenticate(user=user)
