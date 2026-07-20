"""Task models."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.tasks.choices import TaskStatus


class Task(BaseModel):
    """Work item assigned to a studio member."""

    title = models.CharField(_("название"), max_length=200)
    description = models.TextField(_("описание"), blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        verbose_name=_("исполнитель"),
    )
    status = models.CharField(
        _("статус"),
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        db_index=True,
    )
    due_date = models.DateField(_("срок"), blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("задача")
        verbose_name_plural = _("задачи")

    def __str__(self) -> str:
        return self.title
