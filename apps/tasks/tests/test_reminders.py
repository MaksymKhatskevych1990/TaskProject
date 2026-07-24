"""Deadline reminder tests."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task
from apps.tasks.reminders import (
    format_daily_reminder_message,
    format_days_until_deadline,
    format_task_reminder_line,
    list_tasks_with_upcoming_deadlines,
)
from apps.tasks.tasks import send_daily_deadline_reminders

User = get_user_model()


class DeadlineReminderTests(TestCase):
    """Verify deadline countdown formatting and reminder queries."""

    def setUp(self) -> None:
        self.assignee = User.objects.create_user(
            email="assignee@example.com",
            password="pass",
            first_name="Assignee",
            last_name="User",
        )
        self.assignee.telegram_account.chat_id = 123456
        self.assignee.telegram_account.notifications_enabled = True
        self.assignee.telegram_account.save(
            update_fields=["chat_id", "notifications_enabled"]
        )

    def test_format_days_until_deadline_today(self) -> None:
        today = date(2026, 7, 24)
        info = format_days_until_deadline(due_date=today, today=today)

        self.assertEqual(info.label, "срок сегодня")
        self.assertFalse(info.is_overdue)

    def test_format_days_until_deadline_one_day(self) -> None:
        today = date(2026, 7, 24)
        info = format_days_until_deadline(due_date=date(2026, 7, 25), today=today)

        self.assertEqual(info.label, "остался 1 день")

    def test_format_days_until_deadline_overdue(self) -> None:
        today = date(2026, 7, 24)
        info = format_days_until_deadline(due_date=date(2026, 7, 20), today=today)

        self.assertTrue(info.is_overdue)
        self.assertIn("просрочено", info.label)

    def test_list_tasks_with_upcoming_deadlines_filters_open_tasks(self) -> None:
        Task.objects.create(
            title="Open task",
            assignee=self.assignee,
            due_date=date(2026, 7, 25),
            status=TaskStatus.TODO,
            created_by=self.assignee,
            updated_by=self.assignee,
        )
        Task.objects.create(
            title="Done task",
            assignee=self.assignee,
            due_date=date(2026, 7, 25),
            status=TaskStatus.DONE,
            created_by=self.assignee,
            updated_by=self.assignee,
        )

        tasks = list(list_tasks_with_upcoming_deadlines(today=date(2026, 7, 24)))

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Open task")

    def test_format_daily_reminder_message_groups_overdue_and_upcoming(self) -> None:
        overdue = Task.objects.create(
            title="Overdue",
            assignee=self.assignee,
            due_date=date(2026, 7, 20),
            status=TaskStatus.IN_PROGRESS,
            created_by=self.assignee,
            updated_by=self.assignee,
        )
        upcoming = Task.objects.create(
            title="Tomorrow",
            assignee=self.assignee,
            due_date=date(2026, 7, 25),
            status=TaskStatus.TODO,
            created_by=self.assignee,
            updated_by=self.assignee,
        )

        message = format_daily_reminder_message(
            tasks=[overdue, upcoming],
            today=date(2026, 7, 24),
        )

        self.assertIn("Просрочено", message)
        self.assertIn("Overdue", message)
        self.assertIn("Tomorrow", message)
        self.assertIn(format_task_reminder_line(task=upcoming, today=date(2026, 7, 24)), message)

    def test_send_daily_deadline_reminders_queues_messages(self) -> None:
        from unittest.mock import patch

        Task.objects.create(
            title="Due soon",
            assignee=self.assignee,
            due_date=timezone.localdate(),
            status=TaskStatus.TODO,
            created_by=self.assignee,
            updated_by=self.assignee,
        )

        with (
            patch("apps.tasks.tasks.queue_telegram_message") as mock_queue,
            self.settings(TELEGRAM_ENABLED=True),
        ):
            sent_count = send_daily_deadline_reminders()

        self.assertEqual(sent_count, 1)
        mock_queue.assert_called_once()
