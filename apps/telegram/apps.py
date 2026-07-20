"""Telegram application configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegramConfig(AppConfig):
    """Configure the Telegram integration boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.telegram"
    verbose_name = _("Telegram")

    def ready(self) -> None:
        """Register signal handlers."""
        from apps.telegram import signals  # noqa: F401
