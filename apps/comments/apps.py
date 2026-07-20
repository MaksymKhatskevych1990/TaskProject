"""Comments application configuration."""

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """Configure the comments application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comments"
