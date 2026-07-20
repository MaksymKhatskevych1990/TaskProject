"""Dashboard application configuration."""

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """Configure the dashboard application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
