"""Files application configuration."""

from django.apps import AppConfig


class FilesConfig(AppConfig):
    """Configure the files application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.files"
