"""Project service tests."""

from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework.exceptions import ValidationError

from apps.projects import services
from apps.projects.models import normalize_host
from tests.factories.accounts import UserFactory
from tests.factories.projects import ProjectFactory


class ProjectHelperTests(TestCase):
    """Verify project field helpers."""

    def test_normalize_host_strips_scheme_and_path(self) -> None:
        """Domains are stored as a bare hostname."""
        self.assertEqual(
            normalize_host("https://Redwood.studio/admin"), "Redwood.studio"
        )
        self.assertEqual(normalize_host("example.com"), "example.com")


class ProjectNoteServiceTests(TestCase):
    """Verify project notes and Telegram delivery."""

    def test_create_project_note_requires_text(self) -> None:
        """Empty notes are rejected before anything is stored."""
        project = ProjectFactory()
        actor = UserFactory()

        with self.assertRaises(ValidationError):
            services.create_project_note(project=project, body="   ", actor=actor)

        self.assertEqual(project.notes.count(), 0)

    @override_settings(TELEGRAM_ENABLED=True)
    @patch("apps.telegram.services.queue_telegram_message")
    def test_create_project_note_sends_telegram(self, mock_queue) -> None:
        """A note with a Telegram-ready recipient is queued for delivery."""
        project = ProjectFactory(
            name="Redwood", slug="redwood", domain="redwood.studio"
        )
        actor = UserFactory(first_name="Admin", last_name="User")
        recipient = UserFactory(first_name="Ivan", last_name="Petrov")
        account = recipient.telegram_account
        account.chat_id = 123456
        account.notifications_enabled = True
        account.save(update_fields=["chat_id", "notifications_enabled"])

        note = services.create_project_note(
            project=project,
            body="Нужно обновить SSL",
            actor=actor,
            recipient=recipient,
        )

        self.assertTrue(note.telegram_sent)
        self.assertIsNotNone(note.telegram_sent_at)
        mock_queue.assert_called_once()
        text = mock_queue.call_args.kwargs["text"]
        self.assertIn("Redwood", text)
        self.assertIn("Нужно обновить SSL", text)
        self.assertIn("redwood.studio", text)
        self.assertNotIn("server_password", text)

    @override_settings(TELEGRAM_ENABLED=True)
    @patch("apps.telegram.services.queue_telegram_message")
    def test_create_project_note_skips_telegram_without_chat(self, mock_queue) -> None:
        """Notes are still saved when the recipient has no Telegram chat."""
        project = ProjectFactory()
        actor = UserFactory()
        recipient = UserFactory()
        account = recipient.telegram_account
        account.chat_id = None
        account.save(update_fields=["chat_id"])

        note = services.create_project_note(
            project=project,
            body="Проверить деплой",
            actor=actor,
            recipient=recipient,
        )

        self.assertFalse(note.telegram_sent)
        mock_queue.assert_not_called()

    def test_note_message_does_not_include_credentials(self) -> None:
        """Telegram text stays limited to public project context."""
        project = ProjectFactory(
            name="Redwood",
            slug="redwood",
            domain="redwood.studio",
            server_password="super-secret-password",
            extra_credentials="db password 123",
        )
        actor = UserFactory(first_name="Admin", last_name="User")

        text = services.format_project_note_message(
            project=project,
            body="Клиент просит правки",
            actor=actor,
        )

        self.assertNotIn("super-secret-password", text)
        self.assertNotIn("db password 123", text)
        self.assertIn("Клиент просит правки", text)
