"""Task-related choice definitions."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.TextChoices):
    """Lifecycle states for studio tasks."""

    TODO = "todo", _("К выполнению")
    IN_PROGRESS = "in_progress", _("В работе")
    DONE = "done", _("Выполнена")
    CANCELLED = "cancelled", _("Отменена")
