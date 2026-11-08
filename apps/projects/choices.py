"""Project-related choice definitions."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectStatus(models.TextChoices):
    """Lifecycle states for studio projects."""

    DEVELOPMENT = "development", _("В разработке")
    LAUNCHED = "launched", _("Запущен")
    SUPPORT = "support", _("На поддержке")
    PAUSED = "paused", _("Приостановлен")
    ARCHIVED = "archived", _("Архив")
