"""Tests that protect project module boundaries."""

from importlib import import_module

from django.test import SimpleTestCase
from django.urls import resolve

FUTURE_APPLICATIONS = (
    "projects",
    "notifications",
    "comments",
    "dashboard",
    "clients",
    "website",
    "crm",
    "ai",
)

IMPLEMENTED_APPLICATIONS = ("accounts", "employees", "telegram", "tasks", "files")


class ApplicationBoundaryTests(SimpleTestCase):
    """Ensure every planned application exposes a stable API boundary."""

    def test_application_packages_are_importable(self) -> None:
        """Every application has configuration and API modules."""
        for application in FUTURE_APPLICATIONS:
            with self.subTest(application=application):
                import_module(f"apps.{application}.apps")
                api_urls = import_module(f"apps.{application}.api.urls")
                import_module(f"apps.{application}.api.views")
                self.assertEqual(api_urls.urlpatterns, [])

        for application in IMPLEMENTED_APPLICATIONS:
            with self.subTest(application=application):
                import_module(f"apps.{application}.apps")
                import_module(f"apps.{application}.api.urls")
                import_module(f"apps.{application}.api.views")

    def test_versioned_api_and_health_routes_resolve(self) -> None:
        """Core public route boundaries remain available."""
        self.assertEqual(resolve("/health/").url_name, "liveness")
        self.assertEqual(resolve("/api/health/").url_name, "liveness")
        self.assertEqual(
            resolve("/api/v1/auth/token/").url_name,
            "token-obtain",
        )
