"""Accounts application configuration."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configure the accounts application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Учётные записи"

    def ready(self) -> None:
        """Register signal adapters."""
        from apps.accounts import signals  # noqa: F401
