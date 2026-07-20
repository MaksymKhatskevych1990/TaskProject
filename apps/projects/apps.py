"""Projects application configuration."""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Configure the projects application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.projects"
