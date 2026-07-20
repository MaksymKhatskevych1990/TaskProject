"""Website application configuration."""

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """Configure the website application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.website"
