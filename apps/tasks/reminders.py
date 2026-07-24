"""Deadline reminder formatting and queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone

from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task
from apps.telegram.keyboards import project_label

User = get_user_model()

OPEN_STATUSES = (TaskStatus.TODO, TaskStatus.IN_PROGRESS)


@dataclass(frozen=True)
class DeadlineInfo:
    """Human-readable countdown for a task due date."""

    due_date: date
    days_remaining: int
    label: str
    is_overdue: bool


def format_days_until_deadline(*, due_date: date, today: date | None = None) -> DeadlineInfo:
    """Return a Russian label describing how many days remain until the deadline."""
    reference = today or timezone.localdate()
    days_remaining = (due_date - reference).days

    if days_remaining < 0:
        overdue_days = abs(days_remaining)
        label = _pluralize_days(overdue_days, "просрочено на", "просрочено на", "просрочено на")
        return DeadlineInfo(
            due_date=due_date,
            days_remaining=days_remaining,
            label=label,
            is_overdue=True,
        )

    if days_remaining == 0:
        return DeadlineInfo(
            due_date=due_date,
            days_remaining=0,
            label="срок сегодня",
            is_overdue=False,
        )

    if days_remaining == 1:
        return DeadlineInfo(
            due_date=due_date,
            days_remaining=1,
            label="остался 1 день",
            is_overdue=False,
        )

    label = _pluralize_days(days_remaining, "остался", "осталось", "осталось")
    return DeadlineInfo(
        due_date=due_date,
        days_remaining=days_remaining,
        label=label,
        is_overdue=False,
    )


def _pluralize_days(count: int, one: str, few: str, many: str) -> str:
    """Build a Russian phrase with correct day pluralization."""
    remainder_100 = count % 100
    remainder_10 = count % 10
    if 11 <= remainder_100 <= 14:
        prefix = many
    elif remainder_10 == 1:
        prefix = one
    elif 2 <= remainder_10 <= 4:
        prefix = few
    else:
        prefix = many
    return f"{prefix} {count} {_days_word(count)}"


def _days_word(count: int) -> str:
    """Return the correct Russian word for day/days."""
    remainder_100 = count % 100
    remainder_10 = count % 10
    if 11 <= remainder_100 <= 14:
        return "дней"
    if remainder_10 == 1:
        return "день"
    if 2 <= remainder_10 <= 4:
        return "дня"
    return "дней"


def list_tasks_with_upcoming_deadlines(*, today: date | None = None) -> QuerySet[Task]:
    """Return open tasks that have a due date and a Telegram-ready assignee."""
    return (
        Task.objects.filter(
            due_date__isnull=False,
            status__in=OPEN_STATUSES,
            assignee__is_active=True,
            assignee__telegram_account__chat_id__isnull=False,
            assignee__telegram_account__notifications_enabled=True,
        )
        .select_related("assignee", "assignee__telegram_account", "project")
        .order_by("assignee_id", "due_date", "title")
    )


def format_task_reminder_line(*, task: Task, today: date | None = None) -> str:
    """Format a single task line for a daily reminder message."""
    assert task.due_date is not None
    deadline = format_days_until_deadline(due_date=task.due_date, today=today)
    prefix = "🔴" if deadline.is_overdue else "📋"
    due_label = task.due_date.strftime("%d.%m.%Y")
    return (
        f"{prefix} {task.title}\n"
        f"   Проект: {project_label(project=task.project)}\n"
        f"   Срок: {due_label} · {deadline.label}"
    )


def format_daily_reminder_message(*, tasks: list[Task], today: date | None = None) -> str:
    """Build a consolidated daily reminder for one assignee."""
    reference = today or timezone.localdate()
    lines = ["⏰ Напоминание о сроках", ""]
    overdue = [task for task in tasks if task.due_date and task.due_date < reference]
    upcoming = [task for task in tasks if task not in overdue]

    if overdue:
        lines.append(f"Просрочено ({len(overdue)}):")
        for task in overdue:
            lines.append(format_task_reminder_line(task=task, today=reference))
            lines.append("")

    if upcoming:
        if overdue:
            lines.append(f"Предстоящие ({len(upcoming)}):")
        for task in upcoming:
            lines.append(format_task_reminder_line(task=task, today=reference))
            lines.append("")

    return "\n".join(lines).strip()
