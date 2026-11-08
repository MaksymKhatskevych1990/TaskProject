"""Project business operations."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.projects.models import Project, ProjectNote

logger = logging.getLogger(__name__)

User = get_user_model()


def format_project_note_message(
    *,
    project: Project,
    body: str,
    actor: User,
) -> str:
    """Build a Telegram message for a project note. Never include credentials."""
    sender = actor.full_name
    domain = f"\nДомен: {project.domain}" if project.domain else ""
    return (
        f"📌 Заметка по проекту {project.name} ({project.slug}){domain}\n\n"
        f"{body.strip()}\n\n"
        f"От: {sender}"
    )


def send_project_note_to_telegram(
    *,
    project: Project,
    body: str,
    actor: User,
    recipient: User,
) -> bool:
    """Queue a project note for the recipient's Telegram chat."""
    from apps.telegram.models import TelegramAccount
    from apps.telegram.services import queue_telegram_message

    if not settings.TELEGRAM_ENABLED:
        logger.info(
            "Skipped project note Telegram delivery because integration is disabled",
            extra={"project_uuid": str(project.uuid)},
        )
        return False

    account = getattr(recipient, "telegram_account", None)
    if account is None:
        account = TelegramAccount.objects.filter(user=recipient).first()
    if account is None or not account.is_ready_for_notifications:
        logger.info(
            "Skipped project note Telegram delivery",
            extra={
                "project_uuid": str(project.uuid),
                "recipient_uuid": str(recipient.uuid),
            },
        )
        return False

    queue_telegram_message(
        chat_id=account.chat_id,
        text=format_project_note_message(project=project, body=body, actor=actor),
    )
    return True


def create_project_note(
    *,
    project: Project,
    body: str,
    actor: User,
    recipient: User | None = None,
) -> ProjectNote:
    """Store a project note and optionally send it to an employee in Telegram."""
    cleaned_body = body.strip()
    if not cleaned_body:
        raise ValidationError({"body": ["Заметка не может быть пустой."]})

    sent = False
    sent_at = None
    if recipient is not None:
        sent = send_project_note_to_telegram(
            project=project,
            body=cleaned_body,
            actor=actor,
            recipient=recipient,
        )
        if sent:
            sent_at = timezone.now()

    note = ProjectNote.objects.create(
        project=project,
        body=cleaned_body,
        recipient=recipient,
        telegram_sent=sent,
        telegram_sent_at=sent_at,
        created_by=actor,
        updated_by=actor,
    )
    logger.info(
        "Created project note",
        extra={
            "note_uuid": str(note.uuid),
            "project_uuid": str(project.uuid),
            "actor_uuid": str(actor.uuid),
            "telegram_sent": sent,
        },
    )
    return note
