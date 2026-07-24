"""Dashboard read operations."""

from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, QuerySet
from django.urls import reverse
from django.utils import timezone

from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task

User = get_user_model()


@dataclass(frozen=True)
class StatusSummary:
    """Aggregated task count for a single status."""

    status: str
    label: str
    count: int
    color: str
    admin_url: str


@dataclass(frozen=True)
class StudioDashboard:
    """Summary blocks shown on the admin home page."""

    total_tasks: int
    status_summaries: list[StatusSummary]
    overdue_count: int
    overdue_tasks: QuerySet[Task]
    overdue_admin_url: str
    users_without_telegram_count: int
    users_without_telegram: QuerySet[User]
    users_admin_url: str
    telegram_admin_url: str


STATUS_META = {
    TaskStatus.TODO: ("secondary", "К выполнению"),
    TaskStatus.IN_PROGRESS: ("primary", "В работе"),
    TaskStatus.DONE: ("success", "Выполнена"),
    TaskStatus.CANCELLED: ("danger", "Отменена"),
}


def get_studio_dashboard() -> StudioDashboard:
    """Build dashboard metrics for managers and administrators."""
    today = timezone.localdate()
    status_counts = {
        row["status"]: row["count"]
        for row in Task.objects.values("status").annotate(count=Count("id"))
    }
    status_summaries = [
        StatusSummary(
            status=status,
            label=label,
            count=status_counts.get(status, 0),
            color=color,
            admin_url=(
                f"{reverse('admin:tasks_task_changelist')}?status__exact={status}"
            ),
        )
        for status, (color, label) in STATUS_META.items()
    ]

    overdue_tasks = (
        Task.objects.filter(
            due_date__lt=today,
            status__in=[TaskStatus.TODO, TaskStatus.IN_PROGRESS],
        )
        .select_related("assignee")
        .order_by("due_date", "title")[:8]
    )

    users_without_telegram = (
        User.objects.filter(is_active=True)
        .filter(
            Q(telegram_account__isnull=True) | Q(telegram_account__chat_id__isnull=True)
        )
        .select_related("telegram_account")
        .order_by("email")[:8]
    )

    return StudioDashboard(
        total_tasks=Task.objects.count(),
        status_summaries=status_summaries,
        overdue_count=Task.objects.filter(
            due_date__lt=today,
            status__in=[TaskStatus.TODO, TaskStatus.IN_PROGRESS],
        ).count(),
        overdue_tasks=overdue_tasks,
        overdue_admin_url=(
            f"{reverse('admin:tasks_task_changelist')}?due_date__lt={today.isoformat()}"
        ),
        users_without_telegram_count=User.objects.filter(is_active=True)
        .filter(
            Q(telegram_account__isnull=True) | Q(telegram_account__chat_id__isnull=True)
        )
        .count(),
        users_without_telegram=users_without_telegram,
        users_admin_url=reverse("admin:accounts_user_changelist"),
        telegram_admin_url=reverse("admin:telegram_telegramaccount_changelist"),
    )
