"""Telegram discussion routing and message relay."""

from __future__ import annotations

import logging
from math import ceil
from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from apps.comments import selectors as comment_selectors
from apps.comments import services as comment_services
from apps.comments.models import Discussion
from apps.tasks import selectors as task_selectors
from apps.tasks.models import Task
from apps.telegram import client
from apps.telegram.discussion_keyboards import (
    DISCUSSION_PAGE_SIZE,
    PARTNER_PAGE_SIZE,
    build_active_discussion_keyboard,
    build_active_discussion_reply_keyboard,
    build_add_participant_keyboard,
    build_discussion_list_keyboard,
    build_partner_picker_keyboard,
)
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.keyboards import build_main_menu_keyboard, project_label
from apps.telegram.models import TelegramAccount
from apps.telegram.services import (
    _answer_callback,
    _resolve_account_from_chat,
    send_telegram_message,
)

logger = logging.getLogger(__name__)

User = get_user_model()

DRAFT_CACHE_TIMEOUT = 3600
ACTIVE_CACHE_TIMEOUT = 60 * 60 * 24 * 7


def _draft_cache_key(*, chat_id: int) -> str:
    return f"telegram:discussion:draft:{chat_id}"


def _active_cache_key(*, chat_id: int) -> str:
    return f"telegram:discussion:active:{chat_id}"


def _add_draft_cache_key(*, chat_id: int) -> str:
    return f"telegram:discussion:add_draft:{chat_id}"


def get_active_discussion_uuid(*, chat_id: int) -> UUID | None:
    """Return the active discussion UUID for a Telegram chat, if any."""
    raw_value = cache.get(_active_cache_key(chat_id=chat_id))
    if not raw_value:
        return None
    try:
        return UUID(str(raw_value))
    except ValueError:
        return None


def set_active_discussion(*, chat_id: int, discussion_uuid: UUID) -> None:
    """Remember which discussion the user is currently writing to."""
    cache.set(
        _active_cache_key(chat_id=chat_id),
        str(discussion_uuid),
        timeout=ACTIVE_CACHE_TIMEOUT,
    )


def clear_active_discussion(*, chat_id: int) -> None:
    """Leave the active discussion mode for a Telegram chat."""
    cache.delete(_active_cache_key(chat_id=chat_id))


def _get_draft(*, chat_id: int) -> dict[str, Any]:
    draft = cache.get(_draft_cache_key(chat_id=chat_id))
    if not isinstance(draft, dict):
        return {"task_uuid": None, "selected": [], "page": 0}
    draft.setdefault("task_uuid", None)
    draft.setdefault("selected", [])
    draft.setdefault("page", 0)
    return draft


def _save_draft(*, chat_id: int, draft: dict[str, Any]) -> None:
    cache.set(_draft_cache_key(chat_id=chat_id), draft, timeout=DRAFT_CACHE_TIMEOUT)


def clear_draft(*, chat_id: int) -> None:
    cache.delete(_draft_cache_key(chat_id=chat_id))


def _get_add_draft(*, chat_id: int) -> dict[str, Any]:
    draft = cache.get(_add_draft_cache_key(chat_id=chat_id))
    if not isinstance(draft, dict):
        return {"discussion_uuid": None, "selected": [], "page": 0}
    draft.setdefault("discussion_uuid", None)
    draft.setdefault("selected", [])
    draft.setdefault("page", 0)
    return draft


def _save_add_draft(*, chat_id: int, draft: dict[str, Any]) -> None:
    cache.set(_add_draft_cache_key(chat_id=chat_id), draft, timeout=DRAFT_CACHE_TIMEOUT)


def clear_add_draft(*, chat_id: int) -> None:
    cache.delete(_add_draft_cache_key(chat_id=chat_id))


def discussion_title(*, discussion: Discussion) -> str:
    """Return a human-readable discussion title."""
    if discussion.task_id and discussion.task:
        project = project_label(project=discussion.task.project)
        return f"{project} / {discussion.task.title}"
    return "Личный диалог"


def discussion_participant_names(
    *,
    discussion: Discussion,
    viewer: User,
) -> list[str]:
    """Return display names of other discussion participants."""
    names: list[str] = []
    for membership in discussion.memberships.all():
        if membership.user_id == viewer.pk:
            continue
        names.append(membership.user.full_name)
    return names


def discussion_input_placeholder(*, discussion: Discussion, viewer: User) -> str:
    """Return a short hint shown above the message input field."""
    names = discussion_participant_names(discussion=discussion, viewer=viewer)
    if not names:
        return "Сообщение в диалог"
    if len(names) == 1:
        return f"Сообщение для {names[0]}"
    if len(names) == 2:
        return f"Сообщение для {names[0]}, {names[1]}"
    return f"Сообщение для {names[0]}, {names[1]} +{len(names) - 2}"


def format_discussion_context(*, discussion: Discussion, viewer: User) -> str:
    """Build a compact header explaining the active discussion."""
    names = discussion_participant_names(discussion=discussion, viewer=viewer)
    participants = ", ".join(names) if names else "участники"
    return (
        "💬 Активный диалог\n"
        f"С: {participants}\n"
        f"Тема: {discussion_title(discussion=discussion)}"
    )


def format_relay_message(*, discussion: Discussion, author: User, body: str) -> str:
    """Build a relay message sent to other participants."""
    return f"💬 {author.full_name} · {discussion_title(discussion=discussion)}\n{body}"


def send_active_discussion_notice(
    *,
    chat_id: int,
    discussion: Discussion,
    viewer: User,
    intro: str | None = None,
) -> None:
    """Show who the user is talking to and enable the discussion reply keyboard."""
    lines = [format_discussion_context(discussion=discussion, viewer=viewer)]
    if intro:
        lines.extend(["", intro])
    send_telegram_message(
        chat_id=chat_id,
        text="\n".join(lines),
        reply_markup=build_active_discussion_reply_keyboard(
            input_placeholder=discussion_input_placeholder(
                discussion=discussion,
                viewer=viewer,
            )
        ),
    )
    send_telegram_message(
        chat_id=chat_id,
        text="Управление диалогом:",
        reply_markup=build_active_discussion_keyboard(discussion_uuid=discussion.uuid),
    )


def show_discussions_menu(
    *,
    chat_id: int,
    account: TelegramAccount,
    page: int = 0,
    message_id: int | None = None,
) -> None:
    """Send or edit the list of discussions available to the user."""
    queryset = comment_selectors.list_discussions_for_user(user=account.user)
    total_count = queryset.count()
    if total_count == 0:
        text = (
            "💬 Диалоги\n\n"
            "У вас пока нет обсуждений.\n"
            "Нажмите «Новый диалог», чтобы выбрать собеседников."
        )
    else:
        page = max(page, 0)
        total_pages = max(1, ceil(total_count / DISCUSSION_PAGE_SIZE))
        page = min(page, total_pages - 1)
        discussions = list(
            queryset[page * DISCUSSION_PAGE_SIZE : (page + 1) * DISCUSSION_PAGE_SIZE]
        )
        text = (
            "💬 Диалоги\n\n"
            "Выберите обсуждение или создайте новое.\n"
            "Сообщения из активного диалога отправляются выбранным участникам."
        )
        markup = build_discussion_list_keyboard(
            discussions=discussions,
            page=page,
            total_count=total_count,
            viewer=account.user,
        )
        _send_or_edit(chat_id=chat_id, text=text, markup=markup, message_id=message_id)
        return

    markup = build_discussion_list_keyboard(
        discussions=[],
        page=0,
        total_count=0,
        viewer=account.user,
    )
    _send_or_edit(chat_id=chat_id, text=text, markup=markup, message_id=message_id)


def show_partner_picker(
    *,
    chat_id: int,
    account: TelegramAccount,
    page: int | None = None,
    task_uuid: UUID | None = None,
    message_id: int | None = None,
) -> None:
    """Send or edit the participant picker."""
    draft = _get_draft(chat_id=chat_id)
    if task_uuid is not None:
        draft["task_uuid"] = str(task_uuid)
    if page is not None:
        draft["page"] = page
    _save_draft(chat_id=chat_id, draft=draft)

    partners_queryset = comment_selectors.list_discussion_partners(user=account.user)
    total_count = partners_queryset.count()
    if total_count == 0:
        clear_draft(chat_id=chat_id)
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Сейчас нет других пользователей с привязанным Telegram.\n"
                "Попросите коллег написать боту и привязать аккаунт."
            ),
            reply_markup=build_main_menu_keyboard(),
        )
        return

    current_page = max(int(draft.get("page", 0)), 0)
    total_pages = max(1, ceil(total_count / PARTNER_PAGE_SIZE))
    current_page = min(current_page, total_pages - 1)
    draft["page"] = current_page
    _save_draft(chat_id=chat_id, draft=draft)

    partners = list(
        partners_queryset[
            current_page * PARTNER_PAGE_SIZE : (current_page + 1) * PARTNER_PAGE_SIZE
        ]
    )
    selected = set(draft.get("selected", []))

    if draft.get("task_uuid"):
        try:
            task = task_selectors.get_task_by_uuid(UUID(draft["task_uuid"]))
            header = f"Проект: {project_label(project=task.project)}\nЗадача: {task.title}"
        except Task.DoesNotExist:
            header = "Выберите собеседников для обсуждения задачи:"
    else:
        header = "Выберите одного или нескольких собеседников:"

    text = (
        "💬 Новый диалог\n\n"
        f"{header}\n\n"
        "Нажимайте на имена, чтобы отметить участников, затем «Начать»."
    )
    markup = build_partner_picker_keyboard(
        partners=partners,
        selected_user_uuids=selected,
        page=current_page,
        total_count=total_count,
    )
    _send_or_edit(chat_id=chat_id, text=text, markup=markup, message_id=message_id)


def toggle_partner_in_draft(
    *,
    chat_id: int,
    account: TelegramAccount,
    user_uuid: UUID,
    page: int,
    message_id: int,
) -> None:
    """Toggle a user in the participant draft and refresh the picker."""
    draft = _get_draft(chat_id=chat_id)
    selected = set(draft.get("selected", []))
    token = str(user_uuid)
    if token in selected:
        selected.remove(token)
    else:
        selected.add(token)
    draft["selected"] = sorted(selected)
    draft["page"] = page
    _save_draft(chat_id=chat_id, draft=draft)
    show_partner_picker(
        chat_id=chat_id,
        account=account,
        message_id=message_id,
    )


def start_discussion_from_draft(
    *,
    chat_id: int,
    account: TelegramAccount,
    message_id: int,
) -> str | None:
    """Create a discussion from the cached participant draft."""
    draft = _get_draft(chat_id=chat_id)
    selected_uuids = [UUID(value) for value in draft.get("selected", [])]
    task = None
    if draft.get("task_uuid"):
        task = task_selectors.get_task_by_uuid(UUID(draft["task_uuid"]))
        if task.assignee_id != account.user_id and task.created_by_id != account.user_id:
            return "Вы можете обсуждать только задачи, где вы исполнитель или автор."

    try:
        participants = comment_services.resolve_participants_by_uuid(
            creator=account.user,
            participant_uuids=selected_uuids,
        )
        discussion = comment_services.create_discussion(
            creator=account.user,
            participant_users=participants,
            task=task,
        )
    except ValidationError as exc:
        detail = exc.detail
        if isinstance(detail, dict):
            values = next(iter(detail.values()), ["Не удалось создать диалог."])
            message = values[0] if values else "Не удалось создать диалог."
            if isinstance(message, str):
                return message
        return "Не удалось создать диалог."

    clear_draft(chat_id=chat_id)
    activate_discussion_for_participants(discussion=discussion)

    if message_id:
        try:
            client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="💬 Диалог создан.",
                reply_markup={"inline_keyboard": []},
            )
        except (TelegramDisabledError, TelegramAPIError):
            pass

    send_active_discussion_notice(
        chat_id=chat_id,
        discussion=discussion,
        viewer=account.user,
        intro="Пишите сообщения в этот чат — их увидят выбранные коллеги.",
    )
    notify_discussion_started(
        discussion=discussion,
        starter=account.user,
        starter_chat_id=chat_id,
    )
    return None


def activate_discussion_for_participants(*, discussion: Discussion) -> None:
    """Mark the discussion as active for every participant Telegram chat."""
    for membership in discussion.memberships.select_related("user__telegram_account"):
        account = getattr(membership.user, "telegram_account", None)
        if account and account.chat_id:
            set_active_discussion(chat_id=account.chat_id, discussion_uuid=discussion.uuid)


def notify_discussion_started(
    *,
    discussion: Discussion,
    starter: User,
    starter_chat_id: int,
) -> None:
    """Tell other participants that a new discussion has started."""
    discussion = comment_selectors.get_discussion_by_uuid(discussion_uuid=discussion.uuid)
    for membership in discussion.memberships.select_related("user__telegram_account"):
        user = membership.user
        if user.pk == starter.pk:
            continue
        account = getattr(user, "telegram_account", None)
        if not account or not account.chat_id:
            continue
        set_active_discussion(chat_id=account.chat_id, discussion_uuid=discussion.uuid)
        send_active_discussion_notice(
            chat_id=account.chat_id,
            discussion=discussion,
            viewer=user,
            intro=f"{starter.full_name} начал(а) обсуждение. Ответьте в этом чате.",
        )


def show_add_participant_picker(
    *,
    chat_id: int,
    account: TelegramAccount,
    discussion_uuid: UUID,
    page: int | None = None,
    message_id: int | None = None,
) -> str | None:
    """Send or edit the picker for adding participants to an active discussion."""
    try:
        discussion = comment_selectors.get_discussion_for_user(
            discussion_uuid=discussion_uuid,
            user=account.user,
        )
    except Discussion.DoesNotExist:
        return "Обсуждение не найдено."

    draft = _get_add_draft(chat_id=chat_id)
    draft["discussion_uuid"] = str(discussion_uuid)
    if page is not None:
        draft["page"] = page
    _save_add_draft(chat_id=chat_id, draft=draft)

    partners_queryset = comment_selectors.list_addable_partners(
        user=account.user,
        discussion=discussion,
    )
    total_count = partners_queryset.count()
    if total_count == 0:
        clear_add_draft(chat_id=chat_id)
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Нет доступных пользователей для добавления.\n"
                "Все коллеги с Telegram уже в этом диалоге."
            ),
            reply_markup=build_active_discussion_keyboard(
                discussion_uuid=discussion.uuid
            ),
        )
        return None

    current_page = max(int(draft.get("page", 0)), 0)
    total_pages = max(1, ceil(total_count / PARTNER_PAGE_SIZE))
    current_page = min(current_page, total_pages - 1)
    draft["page"] = current_page
    _save_add_draft(chat_id=chat_id, draft=draft)

    partners = list(
        partners_queryset[
            current_page * PARTNER_PAGE_SIZE : (current_page + 1) * PARTNER_PAGE_SIZE
        ]
    )
    selected = set(draft.get("selected", []))

    text = (
        "➕ Добавить участника\n\n"
        f"Тема: {discussion_title(discussion=discussion)}\n\n"
        "Выберите одного или нескольких коллег:"
    )
    markup = build_add_participant_keyboard(
        partners=partners,
        selected_user_uuids=selected,
        page=current_page,
        total_count=total_count,
        discussion_uuid=discussion.uuid,
    )
    _send_or_edit(chat_id=chat_id, text=text, markup=markup, message_id=message_id)
    return None


def toggle_add_participant_in_draft(
    *,
    chat_id: int,
    account: TelegramAccount,
    discussion_uuid: UUID,
    user_uuid: UUID,
    page: int,
    message_id: int,
) -> None:
    """Toggle a user in the add-participant draft and refresh the picker."""
    draft = _get_add_draft(chat_id=chat_id)
    selected = set(draft.get("selected", []))
    token = str(user_uuid)
    if token in selected:
        selected.remove(token)
    else:
        selected.add(token)
    draft["selected"] = sorted(selected)
    draft["page"] = page
    draft["discussion_uuid"] = str(discussion_uuid)
    _save_add_draft(chat_id=chat_id, draft=draft)
    show_add_participant_picker(
        chat_id=chat_id,
        account=account,
        discussion_uuid=discussion_uuid,
        message_id=message_id,
    )


def confirm_add_participants_from_draft(
    *,
    chat_id: int,
    account: TelegramAccount,
    discussion_uuid: UUID,
    message_id: int,
) -> str | None:
    """Add selected users to the discussion from the cached draft."""
    draft = _get_add_draft(chat_id=chat_id)
    selected_uuids = [UUID(value) for value in draft.get("selected", [])]

    try:
        discussion = comment_selectors.get_discussion_for_user(
            discussion_uuid=discussion_uuid,
            user=account.user,
        )
    except Discussion.DoesNotExist:
        clear_add_draft(chat_id=chat_id)
        return "Обсуждение не найдено."

    try:
        participants = comment_services.resolve_participants_by_uuid(
            creator=account.user,
            participant_uuids=selected_uuids,
        )
        discussion = comment_services.add_participants_to_discussion(
            discussion=discussion,
            actor=account.user,
            participant_users=participants,
        )
    except ValidationError as exc:
        detail = exc.detail
        if isinstance(detail, dict):
            values = next(iter(detail.values()), ["Не удалось добавить участников."])
            message = values[0] if values else "Не удалось добавить участников."
            if isinstance(message, str):
                return message
        return "Не удалось добавить участников."

    clear_add_draft(chat_id=chat_id)

    if message_id:
        try:
            client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="✅ Участники добавлены.",
                reply_markup={"inline_keyboard": []},
            )
        except (TelegramDisabledError, TelegramAPIError):
            pass

    notify_participants_added(
        discussion=discussion,
        added_by=account.user,
        added_user_ids={user.pk for user in participants},
    )

    send_active_discussion_notice(
        chat_id=chat_id,
        discussion=discussion,
        viewer=account.user,
        intro="Состав диалога обновлён.",
    )
    return None


def notify_participants_added(
    *,
    discussion: Discussion,
    added_by: User,
    added_user_ids: set[int],
) -> None:
    """Notify newly added participants and refresh active mode for everyone."""
    discussion = comment_selectors.get_discussion_by_uuid(discussion_uuid=discussion.uuid)
    for membership in discussion.memberships.select_related("user__telegram_account"):
        user = membership.user
        account = getattr(user, "telegram_account", None)
        if not account or not account.chat_id:
            continue

        set_active_discussion(chat_id=account.chat_id, discussion_uuid=discussion.uuid)

        if user.pk in added_user_ids:
            send_active_discussion_notice(
                chat_id=account.chat_id,
                discussion=discussion,
                viewer=user,
                intro=f"{added_by.full_name} добавил(а) вас в диалог.",
            )
        elif user.pk != added_by.pk:
            names = [
                member.user.full_name
                for member in discussion.memberships.all()
                if member.user_id in added_user_ids
            ]
            if names:
                send_telegram_message(
                    chat_id=account.chat_id,
                    text=(
                        f"➕ {added_by.full_name} добавил(а) в диалог: "
                        f"{', '.join(names)}"
                    ),
                )


def open_discussion(
    *,
    chat_id: int,
    account: TelegramAccount,
    discussion_uuid: UUID,
    message_id: int,
) -> str | None:
    """Switch the user into an existing discussion."""
    try:
        discussion = comment_selectors.get_discussion_for_user(
            discussion_uuid=discussion_uuid,
            user=account.user,
        )
    except Discussion.DoesNotExist:
        return "Обсуждение не найдено."

    set_active_discussion(chat_id=chat_id, discussion_uuid=discussion.uuid)
    if message_id:
        try:
            client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="💬 Диалог открыт.",
                reply_markup={"inline_keyboard": []},
            )
        except (TelegramDisabledError, TelegramAPIError):
            pass

    send_active_discussion_notice(
        chat_id=chat_id,
        discussion=discussion,
        viewer=account.user,
        intro="Напишите сообщение, чтобы продолжить обсуждение.",
    )
    return None


def stop_discussion(*, chat_id: int, message_id: int | None = None) -> None:
    """Leave the active discussion mode."""
    clear_active_discussion(chat_id=chat_id)
    text = "Диалог завершён. Снова открыть его можно в «💬 Диалоги»."
    if message_id is None:
        send_telegram_message(
            chat_id=chat_id,
            text=text,
            reply_markup=build_main_menu_keyboard(),
        )
        return
    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup={"inline_keyboard": []},
        )
    except (TelegramDisabledError, TelegramAPIError):
        send_telegram_message(
            chat_id=chat_id,
            text=text,
            reply_markup=build_main_menu_keyboard(),
        )


def relay_discussion_message(
    *,
    chat_id: int,
    account: TelegramAccount,
    text: str,
) -> bool:
    """Relay a free-text Telegram message to other discussion participants."""
    discussion_uuid = get_active_discussion_uuid(chat_id=chat_id)
    if discussion_uuid is None:
        return False

    try:
        discussion = comment_selectors.get_discussion_for_user(
            discussion_uuid=discussion_uuid,
            user=account.user,
        )
    except Discussion.DoesNotExist:
        clear_active_discussion(chat_id=chat_id)
        send_telegram_message(
            chat_id=chat_id,
            text="Обсуждение недоступно. Откройте его заново в «💬 Диалоги».",
            reply_markup=build_main_menu_keyboard(),
        )
        return True

    try:
        comment_services.post_discussion_message(
            discussion=discussion,
            author=account.user,
            body=text,
        )
    except ValidationError:
        send_telegram_message(chat_id=chat_id, text="Сообщение не отправлено.")
        return True

    relay_text = format_relay_message(
        discussion=discussion,
        author=account.user,
        body=text.strip(),
    )
    for membership in discussion.memberships.select_related("user__telegram_account"):
        user = membership.user
        if user.pk == account.user_id:
            continue
        recipient = getattr(user, "telegram_account", None)
        if not recipient or not recipient.chat_id:
            continue
        send_telegram_message(
            chat_id=recipient.chat_id,
            text=relay_text,
        )

    return True


def process_discussion_callback(
    *,
    callback_id: str,
    chat_id: int,
    message_id: int,
    callback_query: dict[str, Any],
    payload: dict[str, Any],
) -> None:
    """Handle inline keyboard presses for discussions."""
    account = _resolve_account_from_chat(
        chat_id=chat_id,
        from_user_id=(callback_query.get("from") or {}).get("id"),
    )
    if account is None:
        _answer_callback(callback_id, "Сначала привяжите аккаунт через /start.")
        return

    kind = payload["kind"]
    if kind == "menu":
        show_discussions_menu(
            chat_id=chat_id,
            account=account,
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, "Диалоги")
        return

    if kind == "new":
        clear_draft(chat_id=chat_id)
        show_partner_picker(chat_id=chat_id, account=account, page=0, message_id=message_id)
        _answer_callback(callback_id, "Выбор участников")
        return

    if kind == "task":
        try:
            task = task_selectors.get_task_by_uuid(payload["task_uuid"])
        except Task.DoesNotExist:
            _answer_callback(callback_id, "Задача не найдена.")
            return
        if task.assignee_id != account.user_id and task.created_by_id != account.user_id:
            _answer_callback(callback_id, "Нет доступа к обсуждению этой задачи.")
            return
        clear_draft(chat_id=chat_id)
        show_partner_picker(
            chat_id=chat_id,
            account=account,
            page=0,
            task_uuid=task.uuid,
            message_id=message_id,
        )
        _answer_callback(callback_id, "Выбор участников")
        return

    if kind == "picker_page":
        show_partner_picker(
            chat_id=chat_id,
            account=account,
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, "Страница обновлена")
        return

    if kind == "toggle":
        toggle_partner_in_draft(
            chat_id=chat_id,
            account=account,
            user_uuid=payload["user_uuid"],
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, "Участник обновлён")
        return

    if kind == "start":
        error = start_discussion_from_draft(
            chat_id=chat_id,
            account=account,
            message_id=message_id,
        )
        _answer_callback(callback_id, error or "Диалог создан")
        return

    if kind == "cancel":
        clear_draft(chat_id=chat_id)
        show_discussions_menu(chat_id=chat_id, account=account, message_id=message_id)
        _answer_callback(callback_id, "Отменено")
        return

    if kind == "open":
        error = open_discussion(
            chat_id=chat_id,
            account=account,
            discussion_uuid=payload["discussion_uuid"],
            message_id=message_id,
        )
        _answer_callback(callback_id, error or "Диалог активен")
        return

    if kind == "stop":
        stop_discussion(chat_id=chat_id, message_id=message_id)
        _answer_callback(callback_id, "Диалог завершён")
        return

    if kind == "add":
        error = show_add_participant_picker(
            chat_id=chat_id,
            account=account,
            discussion_uuid=payload["discussion_uuid"],
            page=0,
            message_id=message_id,
        )
        _answer_callback(callback_id, error or "Выбор участников")
        return

    if kind == "add_toggle":
        toggle_add_participant_in_draft(
            chat_id=chat_id,
            account=account,
            discussion_uuid=payload["discussion_uuid"],
            user_uuid=payload["user_uuid"],
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, "Участник обновлён")
        return

    if kind == "add_page":
        error = show_add_participant_picker(
            chat_id=chat_id,
            account=account,
            discussion_uuid=payload["discussion_uuid"],
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, error or "Страница обновлена")
        return

    if kind == "add_confirm":
        error = confirm_add_participants_from_draft(
            chat_id=chat_id,
            account=account,
            discussion_uuid=payload["discussion_uuid"],
            message_id=message_id,
        )
        _answer_callback(callback_id, error or "Участники добавлены")
        return

    if kind == "add_cancel":
        clear_add_draft(chat_id=chat_id)
        try:
            discussion = comment_selectors.get_discussion_for_user(
                discussion_uuid=payload["discussion_uuid"],
                user=account.user,
            )
        except Discussion.DoesNotExist:
            show_discussions_menu(chat_id=chat_id, account=account, message_id=message_id)
            _answer_callback(callback_id, "Отменено")
            return
        if message_id:
            try:
                client.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text="Добавление участников отменено.",
                    reply_markup={"inline_keyboard": []},
                )
            except (TelegramDisabledError, TelegramAPIError):
                pass
        send_active_discussion_notice(
            chat_id=chat_id,
            discussion=discussion,
            viewer=account.user,
        )
        _answer_callback(callback_id, "Отменено")
        return

    _answer_callback(callback_id, "Неизвестная команда.")


def _send_or_edit(
    *,
    chat_id: int,
    text: str,
    markup: dict[str, Any] | None,
    message_id: int | None,
) -> None:
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
