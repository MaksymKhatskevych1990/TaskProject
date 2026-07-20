"""CRM application configuration."""

from django.apps import AppConfig


class CrmConfig(AppConfig):
    """Configure the CRM application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.crm"
