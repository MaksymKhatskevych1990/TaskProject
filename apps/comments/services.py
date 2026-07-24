"""Discussion business operations."""

import logging
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.comments import selectors
from apps.comments.models import Discussion, DiscussionMessage, DiscussionParticipant
from apps.tasks.models import Task

logger = logging.getLogger(__name__)

User = get_user_model()


def create_discussion(
    *,
    creator: User,
    participant_users: list[User],
    task: Task | None = None,
) -> Discussion:
    """Create a discussion and add all participants including the creator."""
    unique_participants = {user.pk: user for user in participant_users if user.pk != creator.pk}
    if not unique_participants:
        raise ValidationError({"participants": ["Выберите хотя бы одного собеседника."]})

    with transaction.atomic():
        discussion = Discussion.objects.create(
            task=task,
            created_by=creator,
            updated_by=creator,
        )

        memberships = [
            DiscussionParticipant(
                discussion=discussion,
                user=creator,
                created_by=creator,
                updated_by=creator,
            )
        ]
        for participant in unique_participants.values():
            memberships.append(
                DiscussionParticipant(
                    discussion=discussion,
                    user=participant,
                    created_by=creator,
                    updated_by=creator,
                )
            )
        DiscussionParticipant.objects.bulk_create(memberships)

    logger.info(
        "Created discussion",
        extra={
            "discussion_uuid": str(discussion.uuid),
            "creator_uuid": str(creator.uuid),
            "participant_count": len(unique_participants) + 1,
            "task_uuid": str(task.uuid) if task else None,
        },
    )
    return selectors.get_discussion_by_uuid(discussion_uuid=discussion.uuid)


def post_discussion_message(
    *,
    discussion: Discussion,
    author: User,
    body: str,
    source: str = DiscussionMessage.Source.TELEGRAM,
) -> DiscussionMessage:
    """Persist a message and bump the discussion timestamp."""
    cleaned_body = body.strip()
    if not cleaned_body:
        raise ValidationError({"body": ["Сообщение не может быть пустым."]})

    if not discussion.memberships.filter(user=author).exists():
        raise ValidationError({"author": ["Пользователь не участвует в обсуждении."]})

    with transaction.atomic():
        message = DiscussionMessage.objects.create(
            discussion=discussion,
            author=author,
            body=cleaned_body,
            source=source,
            created_by=author,
            updated_by=author,
        )
        Discussion.objects.filter(pk=discussion.pk).update(updated_at=timezone.now())

    logger.info(
        "Posted discussion message",
        extra={
            "discussion_uuid": str(discussion.uuid),
            "author_uuid": str(author.uuid),
            "message_uuid": str(message.uuid),
        },
    )
    return message


def get_participants_for_discussion(*, discussion: Discussion) -> list[User]:
    """Return all users participating in the discussion."""
    return [
        membership.user
        for membership in discussion.memberships.select_related(
            "user",
            "user__telegram_account",
        )
    ]


def resolve_participants_by_uuid(
    *,
    creator: User,
    participant_uuids: list[UUID],
) -> list[User]:
    """Return active Telegram-ready users selected for a new discussion."""
    if not participant_uuids:
        raise ValidationError({"participants": ["Выберите хотя бы одного собеседника."]})

    partners = selectors.list_discussion_partners(user=creator)
    selected = list(partners.filter(uuid__in=participant_uuids))
    if len(selected) != len(set(participant_uuids)):
        raise ValidationError({"participants": ["Один или несколько пользователей недоступны."]})
    return selected


def add_participants_to_discussion(
    *,
    discussion: Discussion,
    actor: User,
    participant_users: list[User],
) -> Discussion:
    """Add new participants to an existing discussion."""
    if not discussion.memberships.filter(user=actor).exists():
        raise ValidationError({"actor": ["Вы не участвуете в этом обсуждении."]})

    unique_participants = {
        user.pk: user for user in participant_users if user.pk != actor.pk
    }
    if not unique_participants:
        raise ValidationError({"participants": ["Выберите хотя бы одного нового участника."]})

    existing_ids = set(
        discussion.memberships.values_list("user_id", flat=True)
    )
    new_participants = [
        user for user in unique_participants.values() if user.pk not in existing_ids
    ]
    if not new_participants:
        raise ValidationError({"participants": ["Выбранные пользователи уже в диалоге."]})

    addable = selectors.list_addable_partners(user=actor, discussion=discussion)
    addable_ids = set(addable.values_list("pk", flat=True))
    if not all(user.pk in addable_ids for user in new_participants):
        raise ValidationError({"participants": ["Один или несколько пользователей недоступны."]})

    with transaction.atomic():
        memberships = [
            DiscussionParticipant(
                discussion=discussion,
                user=participant,
                created_by=actor,
                updated_by=actor,
            )
            for participant in new_participants
        ]
        DiscussionParticipant.objects.bulk_create(memberships)
        Discussion.objects.filter(pk=discussion.pk).update(updated_at=timezone.now())

    logger.info(
        "Added participants to discussion",
        extra={
            "discussion_uuid": str(discussion.uuid),
            "actor_uuid": str(actor.uuid),
            "added_count": len(new_participants),
        },
    )
    return selectors.get_discussion_by_uuid(discussion_uuid=discussion.uuid)
