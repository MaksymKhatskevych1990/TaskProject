"""Task service tests."""

from unittest.mock import patch

from django.test import TestCase

from apps.accounts.choices import UserRole
from apps.tasks import services
from tests.factories.accounts import UserFactory


class TaskServiceTests(TestCase):
    """Verify task workflows and Telegram hooks."""

    @patch("apps.tasks.services.telegram_services.notify_user_about_task")
    def test_create_task_notifies_assignee(self, mock_notify) -> None:
        """Creating a task notifies the assignee through Telegram services."""
        actor = UserFactory(role=UserRole.MANAGER)
        assignee = UserFactory()
        mock_notify.return_value = True

        task = services.create_task(
            title="Prepare report",
            description="Monthly summary",
            assignee=assignee,
            actor=actor,
        )

        self.assertEqual(task.title, "Prepare report")
        mock_notify.assert_called_once_with(user=assignee, task=task)

    @patch("apps.tasks.services.telegram_services.notify_user_about_task")
    def test_update_task_notifies_on_reassign(self, mock_notify) -> None:
        """Changing the assignee sends a new Telegram notification."""
        actor = UserFactory(role=UserRole.MANAGER)
        first_assignee = UserFactory()
        second_assignee = UserFactory()
        task = services.create_task(
            title="Review design",
            assignee=first_assignee,
            actor=actor,
            notify=False,
        )
        mock_notify.reset_mock()

        updated = services.update_task(
            task=task,
            data={"assignee": second_assignee},
            actor=actor,
        )

        self.assertEqual(updated.assignee_id, second_assignee.id)
        mock_notify.assert_called_once_with(user=second_assignee, task=updated)
