"""Clients application configuration."""

from django.apps import AppConfig


class ClientsConfig(AppConfig):
    """Configure the clients application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clients"
