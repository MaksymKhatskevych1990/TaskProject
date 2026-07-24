"""Discussion keyboard tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.comments import services
from apps.telegram.discussion_keyboards import build_discussion_list_keyboard

User = get_user_model()


class DiscussionKeyboardTests(TestCase):
    """Verify discussion list keyboard labels."""

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

    def test_personal_discussion_label_uses_partner_name(self) -> None:
        discussion = services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )

        keyboard = build_discussion_list_keyboard(
            discussions=[discussion],
            page=0,
            total_count=1,
            viewer=self.viewer,
        )
        labels = [
            button["text"]
            for row in keyboard["inline_keyboard"]
            for button in row
        ]

        self.assertIn("💬 Dmitriy Bozdrov", labels)

    def test_discussion_list_deduplicates_same_uuid(self) -> None:
        discussion = services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )

        keyboard = build_discussion_list_keyboard(
            discussions=[discussion, discussion],
            page=0,
            total_count=1,
            viewer=self.viewer,
        )
        dialog_labels = [
            button["text"]
            for row in keyboard["inline_keyboard"]
            for button in row
            if button["text"].startswith("💬 ")
        ]

        self.assertEqual(len(dialog_labels), 1)
