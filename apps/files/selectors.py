"""File attachment read operations."""

from uuid import UUID

from django.db.models import QuerySet

from apps.files.models import TaskAttachment
from apps.tasks.models import Task


def get_attachment_by_uuid(*, attachment_uuid: UUID) -> TaskAttachment:
    """Return an attachment with related task and uploader."""
    return TaskAttachment.objects.select_related(
        "task",
        "uploaded_by",
        "created_by",
    ).get(uuid=attachment_uuid)


def list_attachments_for_task(*, task: Task) -> QuerySet[TaskAttachment]:
    """Return attachments for a task ordered by newest first."""
    return TaskAttachment.objects.filter(task=task).select_related(
        "uploaded_by",
        "created_by",
    )
