"""Notifications application configuration."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configure the notifications application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notifications"
