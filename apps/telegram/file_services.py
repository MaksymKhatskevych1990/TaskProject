"""Telegram file upload helpers for task attachments."""

from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from apps.files import selectors as file_selectors
from apps.files import services as file_services
from apps.tasks import selectors as task_selectors
from apps.tasks.models import Task
from apps.telegram import client
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.keyboards import build_task_files_keyboard
from apps.telegram.models import TelegramAccount
from apps.telegram.services import send_telegram_message

logger = logging.getLogger(__name__)

UPLOAD_CACHE_TIMEOUT = 3600


def _upload_cache_key(*, chat_id: int) -> str:
    return f"telegram:task:upload:{chat_id}"


def set_upload_mode(*, chat_id: int, task_uuid: UUID, page: int) -> None:
    """Remember that the next file message should attach to a task."""
    cache.set(
        _upload_cache_key(chat_id=chat_id),
        {"task_uuid": str(task_uuid), "page": page},
        timeout=UPLOAD_CACHE_TIMEOUT,
    )


def clear_upload_mode(*, chat_id: int) -> None:
    """Leave task file upload mode."""
    cache.delete(_upload_cache_key(chat_id=chat_id))


def get_upload_context(*, chat_id: int) -> dict[str, Any] | None:
    """Return cached upload context for a chat, if any."""
    raw = cache.get(_upload_cache_key(chat_id=chat_id))
    return raw if isinstance(raw, dict) else None


def extract_file_from_message(*, message: dict[str, Any]) -> tuple[str, str, str, int] | None:
    """Extract file_id, filename, mime type, and size from a Telegram message."""
    document = message.get("document")
    if document:
        filename = document.get("file_name") or "document"
        mime_type = document.get("mime_type") or "application/octet-stream"
        file_size = int(document.get("file_size") or 0)
        return document["file_id"], filename, mime_type, file_size

    photos = message.get("photo") or []
    if photos:
        largest = photos[-1]
        file_size = int(largest.get("file_size") or 0)
        return largest["file_id"], "photo.jpg", "image/jpeg", file_size

    return None


def format_task_files_message(*, task: Task) -> str:
    """Build a message listing task attachments."""
    attachments = list(file_selectors.list_attachments_for_task(task=task))
    lines = [
        "📎 Файлы задачи",
        "",
        f"Задача: {task.title}",
        f"Проект: {task.project.slug if task.project_id else 'без_проекта'}",
        "",
    ]
    if not attachments:
        lines.append("Пока нет вложений.")
        lines.append("Нажмите «⬆️ Загрузить файл» и отправьте документ или фото.")
    else:
        lines.append(f"Вложений: {len(attachments)}")
        lines.append("")
        for index, attachment in enumerate(attachments[:10], start=1):
            size_kb = max(attachment.file_size // 1024, 1)
            uploader = attachment.uploaded_by.full_name if attachment.uploaded_by else "—"
            lines.append(
                f"{index}. {attachment.original_filename} ({size_kb} КБ, {uploader})"
            )
        if len(attachments) > 10:
            lines.append(f"... и ещё {len(attachments) - 10}")
    return "\n".join(lines)


def show_task_files(
    *,
    chat_id: int,
    task: Task,
    page: int,
    message_id: int | None = None,
) -> None:
    """Send or edit the task attachments screen."""
    from apps.telegram.services import _send_or_edit_history_message

    text = format_task_files_message(task=task)
    markup = build_task_files_keyboard(task=task, page=page)
    _send_or_edit_history_message(
        chat_id=chat_id,
        text=text,
        markup=markup,
        message_id=message_id,
        edit_error_message="Failed to edit Telegram task files message",
    )


def enter_upload_mode(
    *,
    chat_id: int,
    task: Task,
    page: int,
    message_id: int | None = None,
) -> None:
    """Prompt the user to send a file for the selected task."""
    set_upload_mode(chat_id=chat_id, task_uuid=task.uuid, page=page)
    text = (
        "⬆️ Загрузка файла\n\n"
        f"Задача: {task.title}\n\n"
        "Отправьте документ или фото в этот чат — файл будет прикреплён к задаче."
    )
    markup = build_task_files_keyboard(task=task, page=page)
    if message_id is None:
        send_telegram_message(chat_id=chat_id, text=text, reply_markup=markup)
        return
    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=markup,
        )
    except (TelegramDisabledError, TelegramAPIError):
        send_telegram_message(chat_id=chat_id, text=text, reply_markup=markup)


def process_task_file_upload(
    *,
    chat_id: int,
    account: TelegramAccount,
    message: dict[str, Any],
) -> bool:
    """Handle an incoming document/photo as a task attachment."""
    context = get_upload_context(chat_id=chat_id)
    if context is None:
        return False

    file_info = extract_file_from_message(message=message)
    if file_info is None:
        send_telegram_message(
            chat_id=chat_id,
            text="Отправьте документ или фото, чтобы прикрепить файл к задаче.",
        )
        return True

    file_id, filename, mime_type, _file_size = file_info
    task_uuid = UUID(str(context["task_uuid"]))
    page = int(context.get("page", 0))

    try:
        task = task_selectors.get_task_by_uuid(task_uuid)
    except Task.DoesNotExist:
        clear_upload_mode(chat_id=chat_id)
        send_telegram_message(chat_id=chat_id, text="Задача не найдена.")
        return True

    if task.assignee_id != account.user_id and task.created_by_id != account.user_id:
        clear_upload_mode(chat_id=chat_id)
        send_telegram_message(chat_id=chat_id, text="Нет доступа к этой задаче.")
        return True

    try:
        file_meta = client.get_file(file_id=file_id)
        file_path = file_meta.get("file_path")
        if not file_path:
            send_telegram_message(chat_id=chat_id, text="Не удалось получить файл из Telegram.")
            return True
        content = client.download_file(file_path=file_path)
        attachment = file_services.create_task_attachment_from_bytes(
            task=task,
            filename=filename,
            content=content,
            content_type=mime_type,
            actor=account.user,
        )
    except (TelegramDisabledError, TelegramAPIError):
        send_telegram_message(chat_id=chat_id, text="Не удалось скачать файл из Telegram.")
        return True
    except ValidationError as exc:
        detail = exc.detail
        if isinstance(detail, dict):
            values = next(iter(detail.values()), ["Не удалось сохранить файл."])
            error_message = values[0] if values else "Не удалось сохранить файл."
            if isinstance(error_message, str):
                send_telegram_message(chat_id=chat_id, text=error_message)
                return True
        send_telegram_message(chat_id=chat_id, text="Не удалось сохранить файл.")
        return True

    clear_upload_mode(chat_id=chat_id)
    send_telegram_message(
        chat_id=chat_id,
        text=(
            f"✅ Файл «{attachment.original_filename}» прикреплён к задаче «{task.title}»."
        ),
    )
    show_task_files(chat_id=chat_id, task=task, page=page)
    return True
