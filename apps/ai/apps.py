"""AI application configuration."""

from django.apps import AppConfig


class AiConfig(AppConfig):
    """Configure the AI application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai"
