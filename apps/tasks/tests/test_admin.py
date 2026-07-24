"""Task admin tests."""

from django.contrib import admin
from django.test import TestCase

from apps.tasks.admin import TaskAdmin
from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task
from tests.factories.tasks import TaskFactory


class TaskAdminTests(TestCase):
    """Verify task admin presentation reflects stored status."""

    def setUp(self) -> None:
        self.task_admin = TaskAdmin(Task, admin.site)

    def test_status_badge_shows_current_status(self) -> None:
        """Admin badge reads the status saved in the database."""
        task = TaskFactory(status=TaskStatus.DONE)

        html = self.task_admin.status_badge(task)

        self.assertIn("Выполнена", html)
        self.assertIn("#198754", html)

    def test_progress_display_shows_completed_step(self) -> None:
        """Progress label reflects completion from Telegram updates."""
        task = TaskFactory(status=TaskStatus.DONE)

        progress = self.task_admin.progress_display(task)

        self.assertEqual(progress, "3/3 · Выполнена")
