"""Task business operations."""

import logging
from datetime import date
from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.selectors import get_user_by_uuid
from apps.tasks import selectors
from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task
from apps.telegram import services as telegram_services

logger = logging.getLogger(__name__)

User = get_user_model()

TASK_FIELDS = {"title", "description", "status", "due_date"}


def create_task(
    *,
    title: str,
    assignee: User,
    description: str = "",
    status: str = TaskStatus.TODO,
    due_date: date | None = None,
    actor: User,
    notify: bool = True,
) -> Task:
    """Create a task and optionally notify the assignee in Telegram."""
    with transaction.atomic():
        task = Task.objects.create(
            title=title.strip(),
            description=description.strip(),
            assignee=assignee,
            status=status,
            due_date=due_date,
            created_by=actor,
            updated_by=actor,
        )

    logger.info(
        "Created task",
        extra={"task_uuid": str(task.uuid), "assignee_uuid": str(assignee.uuid)},
    )

    if notify:
        telegram_services.notify_user_about_task(user=assignee, task=task)

    return selectors.get_task_by_uuid(task.uuid)


def update_task(
    *,
    task: Task,
    data: dict[str, Any],
    actor: User,
    notify_on_reassign: bool = True,
) -> Task:
    """Update a task and notify when the assignee changes."""
    previous_assignee_id = task.assignee_id
    assignee = data.pop("assignee", None)

    with transaction.atomic():
        if assignee is not None:
            task.assignee = assignee
        for field in TASK_FIELDS:
            if field in data:
                setattr(task, field, data[field])
        task.updated_by = actor
        task.save()

    task = selectors.get_task_by_uuid(task.uuid)

    if notify_on_reassign and assignee is not None and task.assignee_id != previous_assignee_id:
        telegram_services.notify_user_about_task(user=task.assignee, task=task)

    logger.info("Updated task", extra={"task_uuid": str(task.uuid)})
    return task


def assign_task(
    *,
    task: Task,
    assignee_uuid: UUID,
    actor: User,
) -> Task:
    """Reassign a task to another user."""
    assignee = get_user_by_uuid(assignee_uuid)
    if not assignee.is_active:
        raise ValidationError({"assignee": ["Assignee must be an active user."]})
    return update_task(
        task=task,
        data={"assignee": assignee},
        actor=actor,
        notify_on_reassign=True,
    )
