"""Telegram business operations."""

import logging
from typing import Any

from django.contrib.auth import get_user_model

from apps.telegram import client
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.keyboards import build_task_keyboard, parse_task_callback_data
from apps.telegram.models import TelegramAccount
from apps.telegram import selectors as telegram_selectors

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


def send_telegram_message(
    *,
    chat_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
) -> bool:
    """Send a message through the Telegram Bot API."""
    try:
        client.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
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


def queue_telegram_message(
    *,
    chat_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
) -> None:
    """Enqueue a Telegram message for asynchronous delivery."""
    from apps.telegram.tasks import send_telegram_message_task

    send_telegram_message_task.delay(chat_id, text, reply_markup)


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
    callback_query = update.get("callback_query")
    if callback_query:
        process_callback_query(callback_query=callback_query)
        return

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
                "из админки (поле «bot link») и нажмите Start.\n\n"
                f"Ваш chat ID: `{chat_id}`\n"
                "Его можно вписать в админку вручную, если нужно."
            ),
        )
        return

    if text.startswith("/myid"):
        send_telegram_message(
            chat_id=chat_id,
            text=f"Ваш Telegram chat ID: `{chat_id}`",
        )
        return

    if text.startswith("/help"):
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Этот бот отправляет задачи из внутренней системы студии.\n\n"
                "Для привязки аккаунта используйте ссылку из админки.\n"
                "Команды: /myid — показать chat ID, /start <ссылка> — привязать аккаунт.\n"
                "Под задачей есть кнопки «В работе» и «Готово»."
            ),
        )


def process_callback_query(*, callback_query: dict[str, Any]) -> None:
    """Handle inline keyboard presses on task notifications."""
    from apps.tasks import selectors as task_selectors
    from apps.tasks import services as task_services
    from apps.tasks.choices import TaskStatus
    from apps.tasks.models import Task

    callback_id = callback_query.get("id")
    data = (callback_query.get("data") or "").strip()
    message = callback_query.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    message_id = message.get("message_id")

    if not callback_id or chat_id is None or message_id is None:
        return

    parsed = parse_task_callback_data(data)
    if parsed is None:
        _answer_callback(callback_id, "Неизвестная команда.")
        return

    task_uuid, action = parsed
    status_map = {
        "in_progress": TaskStatus.IN_PROGRESS,
        "done": TaskStatus.DONE,
    }
    new_status = status_map.get(action)
    if new_status is None:
        _answer_callback(callback_id, "Действие недоступно.")
        return

    account = telegram_selectors.get_telegram_account_by_chat_id(chat_id=chat_id)
    if account is None:
        _answer_callback(callback_id, "Сначала привяжите аккаунт через /start.")
        return

    try:
        task = task_selectors.get_task_by_uuid(task_uuid)
    except Task.DoesNotExist:
        _answer_callback(callback_id, "Задача не найдена.")
        return

    if task.assignee_id != account.user_id:
        _answer_callback(callback_id, "Эта задача назначена другому пользователю.")
        return

    if task.status in {TaskStatus.DONE, TaskStatus.CANCELLED}:
        _answer_callback(callback_id, "Задача уже закрыта.")
        return

    if task.status == TaskStatus.IN_PROGRESS and action == "in_progress":
        _answer_callback(callback_id, "Задача уже в работе.")
        return

    updated_task = task_services.update_task_status(
        task=task,
        status=new_status,
        actor=account.user,
    )
    text = format_task_notification(task=updated_task)
    keyboard = build_task_keyboard(updated_task)
    markup = keyboard if keyboard is not None else {"inline_keyboard": []}

    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=markup,
        )
    except TelegramDisabledError:
        logger.info("Skipped Telegram message edit because integration is disabled")
    except TelegramAPIError:
        logger.exception("Failed to edit Telegram task message")

    _answer_callback(callback_id, f"Статус: {updated_task.get_status_display()}")


def _answer_callback(callback_id: str, text: str) -> None:
    """Send a toast response for an inline button press."""
    try:
        client.answer_callback_query(callback_query_id=callback_id, text=text)
    except TelegramDisabledError:
        return
    except TelegramAPIError:
        logger.exception("Failed to answer Telegram callback query")


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
    keyboard = build_task_keyboard(task)
    queue_telegram_message(chat_id=account.chat_id, text=text, reply_markup=keyboard)
    return True
