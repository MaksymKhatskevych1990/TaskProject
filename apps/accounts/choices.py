"""Account-related choice definitions."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """Simple role labels used before full RBAC is introduced."""

    ADMIN = "admin", _("Администратор")
    MANAGER = "manager", _("Менеджер")
    EMPLOYEE = "employee", _("Сотрудник")
