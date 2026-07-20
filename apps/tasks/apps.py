"""Tasks application configuration."""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Configure the tasks application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tasks"
    verbose_name = "Задачи"
