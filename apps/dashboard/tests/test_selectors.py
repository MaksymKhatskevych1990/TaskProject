"""Dashboard selector tests."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.dashboard.selectors import get_studio_dashboard
from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task

User = get_user_model()


class StudioDashboardSelectorTests(TestCase):
    """Verify admin dashboard metrics."""

    def test_get_studio_dashboard_counts(self) -> None:
        today = timezone.localdate()
        linked = User.objects.create_user(email="dev1@example.com", password="pass")
        User.objects.create_user(email="dev2@example.com", password="pass")

        linked.telegram_account.chat_id = 12345
        linked.telegram_account.save(update_fields=["chat_id"])

        Task.objects.create(title="Todo task", assignee=linked, status=TaskStatus.TODO)
        Task.objects.create(
            title="In progress", assignee=linked, status=TaskStatus.IN_PROGRESS
        )
        Task.objects.create(title="Done", assignee=linked, status=TaskStatus.DONE)
        Task.objects.create(
            title="Overdue",
            assignee=linked,
            status=TaskStatus.TODO,
            due_date=today - timedelta(days=2),
        )

        dashboard = get_studio_dashboard()

        self.assertEqual(dashboard.total_tasks, 4)
        self.assertEqual(dashboard.overdue_count, 1)
        self.assertEqual(dashboard.users_without_telegram_count, 1)

        status_map = {item.status: item.count for item in dashboard.status_summaries}
        self.assertEqual(status_map[TaskStatus.TODO], 2)
        self.assertEqual(status_map[TaskStatus.IN_PROGRESS], 1)
        self.assertEqual(status_map[TaskStatus.DONE], 1)
        self.assertEqual(status_map[TaskStatus.CANCELLED], 0)

        self.assertIn("/admin/tasks/task/", dashboard.overdue_admin_url)
        self.assertIn("/admin/accounts/user/", dashboard.users_admin_url)
