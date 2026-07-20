"""Telegram service tests."""

from unittest.mock import patch

from django.test import TestCase, override_settings

from apps.telegram import services
from apps.telegram.models import TelegramAccount
from tests.factories.accounts import UserFactory
from tests.factories.tasks import TaskFactory
from tests.factories.telegram import TelegramAccountFactory


class TelegramServiceTests(TestCase):
    """Verify Telegram linking and notification helpers."""

    @patch("apps.telegram.services.send_telegram_message")
    def test_link_account_by_token_updates_chat(self, mock_send) -> None:
        """A valid start token binds the Telegram chat to a studio user."""
        account = TelegramAccountFactory(chat_id=None, username="")
        account.chat_id = None
        account.username = ""
        account.save(update_fields=["chat_id", "username"])
        mock_send.return_value = True

        linked = services.link_account_by_token(
            token=str(account.link_token),
            chat_id=999888777,
            username="linked_user",
        )

        self.assertIsNotNone(linked)
        linked.refresh_from_db()
        self.assertEqual(linked.chat_id, 999888777)
        self.assertEqual(linked.username, "linked_user")
        self.assertTrue(linked.notifications_enabled)

    @patch("apps.telegram.services.queue_telegram_message")
    def test_notify_user_about_task_queues_message(self, mock_queue) -> None:
        """Task notifications are queued for ready Telegram accounts."""
        user = UserFactory()
        account = user.telegram_account
        account.chat_id = 12345
        account.notifications_enabled = True
        account.save(update_fields=["chat_id", "notifications_enabled"])
        task = TaskFactory(assignee=user)

        sent = services.notify_user_about_task(user=user, task=task)

        self.assertTrue(sent)
        mock_queue.assert_called_once()
        self.assertIn(task.title, mock_queue.call_args.kwargs["text"])
        self.assertIn("inline_keyboard", mock_queue.call_args.kwargs["reply_markup"])

    @patch("apps.telegram.services.client.edit_message_text")
    @patch("apps.telegram.services.client.answer_callback_query")
    def test_process_callback_query_marks_task_done(
        self,
        mock_answer,
        mock_edit,
    ) -> None:
        """Assignee can mark a task as done from Telegram buttons."""
        user = UserFactory()
        account = user.telegram_account
        account.chat_id = 555001
        account.save(update_fields=["chat_id"])
        task = TaskFactory(assignee=user, status="todo")
        callback_data = f"task:{task.uuid}:done"

        services.process_callback_query(
            callback_query={
                "id": "cb-1",
                "data": callback_data,
                "message": {"chat": {"id": 555001}, "message_id": 77},
            }
        )

        task.refresh_from_db()
        self.assertEqual(task.status, "done")
        mock_edit.assert_called_once()
        mock_answer.assert_called_once()

    @patch("apps.telegram.services.client.answer_callback_query")
    def test_process_callback_query_rejects_other_assignee(self, mock_answer) -> None:
        """Users cannot change tasks assigned to someone else."""
        assignee = UserFactory()
        other = UserFactory()
        account = other.telegram_account
        account.chat_id = 555002
        account.save(update_fields=["chat_id"])
        task = TaskFactory(assignee=assignee, status="todo")

        services.process_callback_query(
            callback_query={
                "id": "cb-2",
                "data": f"task:{task.uuid}:done",
                "message": {"chat": {"id": 555002}, "message_id": 88},
            }
        )

        task.refresh_from_db()
        self.assertEqual(task.status, "todo")
        mock_answer.assert_called_once()
        self.assertIn("другому", mock_answer.call_args.kwargs["text"])

    def test_format_task_notification_in_russian(self) -> None:
        """Task messages include title and status labels."""
        task = TaskFactory(title="Deploy release")

        message = services.format_task_notification(task=task)

        self.assertIn("Deploy release", message)
        self.assertIn("Новая задача", message)
        self.assertIn("Статус:", message)

    @override_settings(TELEGRAM_ENABLED=False, TELEGRAM_BOT_TOKEN="")
    def test_send_telegram_message_skips_when_disabled(self) -> None:
        """Disabled integration does not call the Telegram API."""
        sent = services.send_telegram_message(chat_id=1, text="hello")
        self.assertFalse(sent)

    @patch("apps.telegram.services.link_account_by_token")
    def test_process_webhook_start_command(self, mock_link) -> None:
        """Webhook updates with /start token trigger account linking."""
        services.process_webhook_update(
            update={
                "message": {
                    "text": "/start test-token",
                    "chat": {"id": 42},
                    "from": {"username": "worker"},
                }
            }
        )

        mock_link.assert_called_once_with(
            token="test-token",
            chat_id=42,
            username="worker",
        )
