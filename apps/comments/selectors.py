"""Discussion read operations."""

from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet

from apps.comments.models import Discussion, DiscussionMessage, DiscussionParticipant

User = get_user_model()


def get_discussion_by_uuid(*, discussion_uuid: UUID) -> Discussion:
    """Return a discussion with related task and participants."""
    return (
        Discussion.objects.select_related("task", "task__project", "created_by")
        .prefetch_related(
            Prefetch(
                "memberships",
                queryset=DiscussionParticipant.objects.select_related(
                    "user",
                    "user__telegram_account",
                ),
            )
        )
        .get(uuid=discussion_uuid)
    )


def get_discussion_for_user(*, discussion_uuid: UUID, user: User) -> Discussion:
    """Return a discussion only if the user participates in it."""
    return (
        Discussion.objects.filter(uuid=discussion_uuid, memberships__user=user)
        .select_related("task", "task__project", "created_by")
        .prefetch_related(
            Prefetch(
                "memberships",
                queryset=DiscussionParticipant.objects.select_related(
                    "user",
                    "user__telegram_account",
                ),
            )
        )
        .get()
    )


def list_discussions_for_user(*, user: User) -> QuerySet[Discussion]:
    """Return active discussions where the user is a participant."""
    return (
        Discussion.objects.filter(is_active=True, memberships__user=user)
        .select_related("task", "task__project", "created_by")
        .prefetch_related(
            Prefetch(
                "memberships",
                queryset=DiscussionParticipant.objects.select_related(
                    "user",
                    "user__telegram_account",
                ),
            )
        )
        .order_by("-updated_at")
        .distinct()
    )


def list_discussion_messages(*, discussion: Discussion) -> QuerySet[DiscussionMessage]:
    """Return messages for a discussion."""
    return DiscussionMessage.objects.filter(discussion=discussion).select_related(
        "author"
    )


def list_discussion_partners(*, user: User) -> QuerySet[User]:
    """Return active users with Telegram who can join a bot discussion."""
    return (
        User.objects.filter(
            is_active=True,
            telegram_account__chat_id__isnull=False,
            telegram_account__notifications_enabled=True,
        )
        .exclude(pk=user.pk)
        .select_related("telegram_account", "profile")
        .order_by("email")
    )


def list_addable_partners(*, user: User, discussion: Discussion) -> QuerySet[User]:
    """Return Telegram-ready users who are not yet in the discussion."""
    member_ids = discussion.memberships.values_list("user_id", flat=True)
    return list_discussion_partners(user=user).exclude(pk__in=member_ids)
