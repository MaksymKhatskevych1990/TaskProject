"""Discussion service tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.comments import services
from apps.comments.models import DiscussionMessage
from apps.tasks.models import Task

User = get_user_model()


class DiscussionServiceTests(TestCase):
    """Verify discussion creation and messaging."""

    def setUp(self) -> None:
        self.creator = User.objects.create_user(
            email="creator@example.com",
            password="pass",
            first_name="Creator",
            last_name="User",
        )
        self.partner = User.objects.create_user(
            email="partner@example.com",
            password="pass",
            first_name="Partner",
            last_name="User",
        )
        self.partner.telegram_account.chat_id = 123456
        self.partner.telegram_account.notifications_enabled = True
        self.partner.telegram_account.save(
            update_fields=["chat_id", "notifications_enabled"]
        )
        self.task = Task.objects.create(
            title="Landing page",
            assignee=self.creator,
            created_by=self.creator,
            updated_by=self.creator,
        )

    def test_create_discussion_adds_creator_and_partners(self) -> None:
        discussion = services.create_discussion(
            creator=self.creator,
            participant_users=[self.partner],
            task=self.task,
        )

        self.assertEqual(discussion.memberships.count(), 2)
        self.assertTrue(
            discussion.memberships.filter(user=self.creator).exists()
        )
        self.assertTrue(
            discussion.memberships.filter(user=self.partner).exists()
        )

    def test_create_discussion_requires_partner(self) -> None:
        with self.assertRaises(ValidationError):
            services.create_discussion(
                creator=self.creator,
                participant_users=[],
                task=self.task,
            )

    def test_post_discussion_message_persists_body(self) -> None:
        discussion = services.create_discussion(
            creator=self.creator,
            participant_users=[self.partner],
        )

        message = services.post_discussion_message(
            discussion=discussion,
            author=self.creator,
            body="  Нужно уточнить макет  ",
        )

        self.assertEqual(message.body, "Нужно уточнить макет")
        self.assertEqual(DiscussionMessage.objects.count(), 1)

    def test_add_participants_to_discussion(self) -> None:
        third_user = User.objects.create_user(
            email="third@example.com",
            password="pass",
            first_name="Third",
            last_name="User",
        )
        third_user.telegram_account.chat_id = 789012
        third_user.telegram_account.notifications_enabled = True
        third_user.telegram_account.save(
            update_fields=["chat_id", "notifications_enabled"]
        )

        discussion = services.create_discussion(
            creator=self.creator,
            participant_users=[self.partner],
        )

        updated = services.add_participants_to_discussion(
            discussion=discussion,
            actor=self.creator,
            participant_users=[third_user],
        )

        self.assertEqual(updated.memberships.count(), 3)
        self.assertTrue(
            updated.memberships.filter(user=third_user).exists()
        )

    def test_add_participants_rejects_existing_member(self) -> None:
        discussion = services.create_discussion(
            creator=self.creator,
            participant_users=[self.partner],
        )

        with self.assertRaises(ValidationError):
            services.add_participants_to_discussion(
                discussion=discussion,
                actor=self.creator,
                participant_users=[self.partner],
            )
