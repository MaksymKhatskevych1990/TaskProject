"""File attachment models."""

import uuid as uuid_lib

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


def task_attachment_upload_to(instance: "TaskAttachment", filename: str) -> str:
    """Store attachments under a task-specific prefix."""
    safe_name = filename.replace("/", "_").replace("\\", "_")
    return f"tasks/{instance.task.uuid}/{uuid_lib.uuid4()}_{safe_name}"


class TaskAttachment(BaseModel):
    """File attached to a studio task."""

    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("задача"),
    )
    file = models.FileField(
        _("файл"),
        upload_to=task_attachment_upload_to,
    )
    original_filename = models.CharField(_("имя файла"), max_length=255)
    content_type = models.CharField(_("тип"), max_length=128, blank=True)
    file_size = models.PositiveIntegerField(_("размер"), default=0)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="uploaded_task_attachments",
        verbose_name=_("загрузил"),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("вложение задачи")
        verbose_name_plural = _("вложения задач")

    def __str__(self) -> str:
        return self.original_filename
