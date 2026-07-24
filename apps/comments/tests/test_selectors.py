"""Discussion selector tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.comments import selectors, services
from apps.comments.models import DiscussionMessage

User = get_user_model()


class DiscussionSelectorTests(TestCase):
    """Verify discussion queries do not return duplicates."""

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

    def test_list_discussions_for_user_does_not_duplicate_with_messages(self) -> None:
        discussion = services.create_discussion(
            creator=self.viewer,
            participant_users=[self.partner],
        )
        services.post_discussion_message(
            discussion=discussion,
            author=self.viewer,
            body="Первое сообщение",
        )
        services.post_discussion_message(
            discussion=discussion,
            author=self.partner,
            body="Второе сообщение",
        )

        discussions = list(selectors.list_discussions_for_user(user=self.viewer))

        self.assertEqual(len(discussions), 1)
        self.assertEqual(DiscussionMessage.objects.filter(discussion=discussion).count(), 2)
