"""Telegram business operations."""

import logging
from typing import Any

from django.contrib.auth import get_user_model

from apps.telegram import client
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.models import TelegramAccount

logger = logging.getLogger(__name__)

User = get_user_model()

TELEGRAM_FIELDS = {"telegram_username", "telegram_chat_id", "telegram_notifications_enabled"}


def normalize_username(value: str) -> str:
    """Store Telegram usernames without the leading @ symbol."""
    return value.strip().lstrip("@")


def ensure_telegram_account(*, user: User) -> TelegramAccount:
    """Create a Telegram account record when one does not exist yet."""
    account, created = TelegramAccount.objects.get_or_create(user=user)
    if created:
        logger.info(
            "Created Telegram account placeholder",
            extra={"user_uuid": str(user.uuid)},
        )
    return account


def update_telegram_account(
    *,
    user: User,
    data: dict[str, Any],
    actor: User | None = None,
) -> TelegramAccount:
    """Update Telegram contact data for a user."""
    account = ensure_telegram_account(user=user)
    updates: dict[str, Any] = {}

    if "telegram_username" in data:
        updates["username"] = normalize_username(data["telegram_username"])
    if "telegram_chat_id" in data:
        updates["chat_id"] = data["telegram_chat_id"]
    if "telegram_notifications_enabled" in data:
        updates["notifications_enabled"] = data["telegram_notifications_enabled"]

    if not updates:
        return account

    for field, value in updates.items():
        setattr(account, field, value)
    if actor is not None:
        account.updated_by = actor
    account.save()
    logger.info(
        "Updated Telegram account",
        extra={"user_uuid": str(user.uuid), "chat_id": account.chat_id},
    )
    return account


def send_telegram_message(*, chat_id: int, text: str) -> bool:
    """Send a message through the Telegram Bot API."""
    try:
        client.send_message(chat_id=chat_id, text=text)
    except TelegramDisabledError:
        logger.info(
            "Skipped Telegram message because integration is disabled",
            extra={"chat_id": chat_id},
        )
        return False
    except TelegramAPIError:
        logger.exception("Failed to send Telegram message", extra={"chat_id": chat_id})
        raise
    return True


def queue_telegram_message(*, chat_id: int, text: str) -> None:
    """Enqueue a Telegram message for asynchronous delivery."""
    from apps.telegram.tasks import send_telegram_message_task

    send_telegram_message_task.delay(chat_id, text)


def link_account_by_token(
    *,
    token: str,
    chat_id: int,
    username: str = "",
) -> TelegramAccount | None:
    """Bind a Telegram chat to a studio user using a one-time link token."""
    account = (
        TelegramAccount.objects.select_related("user")
        .filter(link_token=token)
        .first()
    )
    if account is None:
        send_telegram_message(
            chat_id=chat_id,
            text="Ссылка недействительна. Попросите администратора прислать новую.",
        )
        return None

    update_telegram_account(
        user=account.user,
        data={
            "telegram_chat_id": chat_id,
            "telegram_username": username,
            "telegram_notifications_enabled": True,
        },
    )
    account.refresh_from_db()
    send_telegram_message(
        chat_id=chat_id,
        text=(
            f"Аккаунт привязан к {account.user.email}.\n"
            "Теперь вы будете получать задачи в этот чат."
        ),
    )
    return account


def process_webhook_update(*, update: dict[str, Any]) -> None:
    """Handle an incoming Telegram update."""
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None:
        return

    text = (message.get("text") or "").strip()
    from_user = message.get("from") or {}
    username = from_user.get("username") or ""

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        token = parts[1].strip() if len(parts) > 1 else ""
        if token:
            link_account_by_token(token=token, chat_id=chat_id, username=username)
            return
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Привет! Чтобы получать задачи, откройте персональную ссылку "
                "из админки или попросите её у администратора."
            ),
        )
        return

    if text.startswith("/help"):
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Этот бот отправляет задачи из внутренней системы студии.\n\n"
                "Для привязки аккаунта используйте ссылку вида "
                "https://t.me/<bot>?start=<token> из админки."
            ),
        )


def format_task_notification(*, task: Any) -> str:
    """Build a Russian notification message for a task assignment."""
    lines = [
        "📋 Новая задача",
        "",
        f"Название: {task.title}",
    ]
    if task.description:
        lines.extend(["", f"Описание: {task.description}"])
    if task.due_date:
        lines.append(f"Срок: {task.due_date.strftime('%d.%m.%Y')}")
    lines.append(f"Статус: {task.get_status_display()}")
    return "\n".join(lines)


def notify_user_about_task(*, user: User, task: Any) -> bool:
    """Send a task notification to the assignee's Telegram chat."""
    account = getattr(user, "telegram_account", None)
    if account is None:
        account = TelegramAccount.objects.filter(user=user).first()
    if account is None or not account.is_ready_for_notifications:
        logger.info(
            "Skipped Telegram task notification",
            extra={"user_uuid": str(user.uuid), "task_uuid": str(task.uuid)},
        )
        return False

    text = format_task_notification(task=task)
    queue_telegram_message(chat_id=account.chat_id, text=text)
    return True
