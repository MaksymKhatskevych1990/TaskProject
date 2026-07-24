"""Task read operations."""

from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.tasks.models import Task

User = get_user_model()


def get_task_by_uuid(task_uuid: UUID) -> Task:
    """Return a task with related users preloaded."""
    return Task.objects.select_related(
        "assignee",
        "created_by",
        "updated_by",
        "project",
    ).get(uuid=task_uuid)


def list_tasks(
    *,
    assignee: User | None = None,
    project=None,
    unassigned_only: bool = False,
    status: str | None = None,
) -> QuerySet[Task]:
    """Return tasks ordered by newest first."""
    queryset = Task.objects.select_related(
        "assignee",
        "created_by",
        "updated_by",
        "project",
    ).order_by("-created_at")
    if assignee is not None:
        queryset = queryset.filter(assignee=assignee)
    if unassigned_only:
        queryset = queryset.filter(project__isnull=True)
    elif project is not None:
        queryset = queryset.filter(project=project)
    if status:
        queryset = queryset.filter(status=status)
    return queryset
