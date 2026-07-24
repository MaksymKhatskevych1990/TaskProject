"""Discussion formatting tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.comments import services as comment_services
from apps.telegram.discussion_keyboards import (
    DISCUSSION_STOP_BUTTON,
    build_active_discussion_reply_keyboard,
)
from apps.telegram.discussion_services import (
    discussion_input_placeholder,
    format_discussion_context,
    format_relay_message,
)

User = get_user_model()


class DiscussionFormattingTests(TestCase):
    """Verify compact discussion labels for Telegram."""

    def setUp(self) -> None:
        self.viewer = User.objects.create_user(
            email="viewer@example.com",
            password="pass",
            first_name="Viewer",
            last_name="User",
        )
        self.partner = User.objects.create_user(
            email="partner@example.com",
            password="pass",
            first_name="Dmitriy",
            last_name="Bozdrov",
        )

    def test_format_relay_message_is_compact(self) -> None:
        discussion = comment_services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )

        message = format_relay_message(
            discussion=discussion,
            author=self.partner,
            body="да тут)",
        )

        self.assertIn("Dmitriy Bozdrov", message)
        self.assertIn("да тут)", message)
        self.assertNotIn("──────────", message)
        self.assertNotIn("От:", message)

    def test_discussion_input_placeholder_for_single_partner(self) -> None:
        discussion = comment_services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )

        placeholder = discussion_input_placeholder(
            discussion=discussion,
            viewer=self.viewer,
        )

        self.assertEqual(placeholder, "Сообщение для Dmitriy Bozdrov")

    def test_active_discussion_reply_keyboard_has_placeholder(self) -> None:
        keyboard = build_active_discussion_reply_keyboard(
            input_placeholder="Сообщение для Dmitriy Bozdrov"
        )

        self.assertEqual(
            keyboard["keyboard"][0][0]["text"],
            DISCUSSION_STOP_BUTTON,
        )
        self.assertEqual(
            keyboard["input_field_placeholder"],
            "Сообщение для Dmitriy Bozdrov",
        )

    def test_format_discussion_context_lists_participants(self) -> None:
        discussion = comment_services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )

        context = format_discussion_context(
            discussion=discussion,
            viewer=self.viewer,
        )

        self.assertIn("С: Dmitriy Bozdrov", context)
        self.assertIn("Тема: Личный диалог", context)
