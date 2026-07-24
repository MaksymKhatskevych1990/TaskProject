"""Dashboard application configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DashboardConfig(AppConfig):
    """Configure the dashboard application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = _("Дашборд")

    def ready(self) -> None:
        """Register the admin dashboard widgets."""
        from apps.dashboard.admin_hooks import register_admin_dashboard

        register_admin_dashboard()
