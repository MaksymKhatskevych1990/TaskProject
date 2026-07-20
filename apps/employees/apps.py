"""Employees application configuration."""

from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    """Configure the employees application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.employees"
    verbose_name = "Сотрудники"
