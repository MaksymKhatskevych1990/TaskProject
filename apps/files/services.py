"""File attachment business operations."""

import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.files import selectors
from apps.files.models import TaskAttachment
from apps.tasks.models import Task

logger = logging.getLogger(__name__)

User = get_user_model()

MAX_ATTACHMENT_SIZE = 20 * 1024 * 1024  # 20 MB


def create_task_attachment(
    *,
    task: Task,
    uploaded_file: Any,
    actor: User,
) -> TaskAttachment:
    """Persist an uploaded file for a task."""
    original_filename = getattr(uploaded_file, "name", "") or "file"
    content_type = getattr(uploaded_file, "content_type", "") or ""
    file_size = getattr(uploaded_file, "size", 0) or 0

    if file_size > MAX_ATTACHMENT_SIZE:
        raise ValidationError(
            {"file": [f"Файл слишком большой. Максимум {MAX_ATTACHMENT_SIZE // (1024 * 1024)} МБ."]}
        )

    with transaction.atomic():
        attachment = TaskAttachment.objects.create(
            task=task,
            original_filename=original_filename,
            content_type=content_type,
            file_size=file_size,
            uploaded_by=actor,
            created_by=actor,
            updated_by=actor,
        )
        attachment.file.save(original_filename, uploaded_file, save=True)

    logger.info(
        "Created task attachment",
        extra={
            "task_uuid": str(task.uuid),
            "attachment_uuid": str(attachment.uuid),
            "attachment_filename": original_filename,
        },
    )
    return selectors.get_attachment_by_uuid(attachment_uuid=attachment.uuid)


def create_task_attachment_from_bytes(
    *,
    task: Task,
    filename: str,
    content: bytes,
    content_type: str = "",
    actor: User,
) -> TaskAttachment:
    """Create a task attachment from raw bytes (e.g. Telegram download)."""
    if len(content) > MAX_ATTACHMENT_SIZE:
        raise ValidationError(
            {"file": [f"Файл слишком большой. Максимум {MAX_ATTACHMENT_SIZE // (1024 * 1024)} МБ."]}
        )

    uploaded_file = ContentFile(content, name=filename)
    uploaded_file.content_type = content_type
    uploaded_file.size = len(content)
    return create_task_attachment(task=task, uploaded_file=uploaded_file, actor=actor)


def delete_task_attachment(*, attachment: TaskAttachment, actor: User) -> None:
    """Remove a task attachment and its stored file."""
    task_uuid = str(attachment.task.uuid)
    attachment_uuid = str(attachment.uuid)
    filename = attachment.original_filename
    attachment.file.delete(save=False)
    attachment.delete()
    logger.info(
        "Deleted task attachment",
        extra={
            "task_uuid": task_uuid,
            "attachment_uuid": attachment_uuid,
            "attachment_filename": filename,
            "actor_uuid": str(actor.uuid),
        },
    )
