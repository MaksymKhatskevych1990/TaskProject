"""Telegram inline keyboards for discussions."""

from math import ceil
from typing import Any
from uuid import UUID

DISCUSSION_PAGE_SIZE = 5
PARTNER_PAGE_SIZE = 5

MENU_DIALOGS_BUTTON = "💬 Диалоги"
DISCUSSION_STOP_BUTTON = "🔚 Завершить диалог"


def build_discussion_menu_callback(*, page: int = 0) -> str:
    """Build callback data for the discussion list."""
    return f"dsc:mn:{page}"


def build_discussion_new_callback() -> str:
    """Build callback data for starting a new discussion picker."""
    return "dsc:new"


def build_discussion_task_callback(*, task_uuid: UUID, page: int) -> str:
    """Build callback data for picking participants for a task discussion."""
    return f"dsc:tk:{page}:{task_uuid}"


def build_discussion_open_callback(*, discussion_uuid: UUID) -> str:
    """Build callback data for opening a discussion."""
    return f"dsc:op:{discussion_uuid}"


def build_discussion_toggle_callback(*, user_uuid: UUID, page: int) -> str:
    """Build callback data for toggling a participant in the draft picker."""
    return f"dsc:tg:{page}:{user_uuid}"


def build_discussion_picker_page_callback(*, page: int) -> str:
    """Build callback data for paginating the participant picker."""
    return f"dsc:pg:{page}"


def build_discussion_start_callback(*, page: int) -> str:
    """Build callback data for creating a discussion from the draft."""
    return f"dsc:st:{page}"


def build_discussion_cancel_callback() -> str:
    """Build callback data for cancelling the participant picker."""
    return "dsc:cn"


def build_discussion_stop_callback() -> str:
    """Build callback data for leaving the active discussion mode."""
    return "dsc:sp"


def build_discussion_add_callback(*, discussion_uuid: UUID) -> str:
    """Build callback data for adding participants to an active discussion."""
    return f"dsc:ad:{discussion_uuid}"


def build_discussion_add_toggle_callback(
    *,
    discussion_uuid: UUID,
    user_uuid: UUID,
    page: int,
) -> str:
    """Build callback data for toggling a user in the add-participant draft."""
    return f"dsc:at:{page}:{discussion_uuid}:{user_uuid}"


def build_discussion_add_page_callback(*, discussion_uuid: UUID, page: int) -> str:
    """Build callback data for paginating the add-participant picker."""
    return f"dsc:ap:{page}:{discussion_uuid}"


def build_discussion_add_confirm_callback(*, discussion_uuid: UUID, page: int) -> str:
    """Build callback data for confirming new participants."""
    return f"dsc:ac:{page}:{discussion_uuid}"


def build_discussion_add_cancel_callback(*, discussion_uuid: UUID) -> str:
    """Build callback data for cancelling the add-participant flow."""
    return f"dsc:ax:{discussion_uuid}"


def parse_discussion_callback(data: str) -> dict[str, Any] | None:
    """Parse callback data emitted by discussion keyboards."""
    parts = data.split(":")
    if len(parts) < 2 or parts[0] != "dsc":
        return None

    kind = parts[1]
    if kind == "mn" and len(parts) == 3:
        try:
            return {"kind": "menu", "page": int(parts[2])}
        except ValueError:
            return None

    if kind == "new" and len(parts) == 2:
        return {"kind": "new"}

    if kind == "tk" and len(parts) == 4:
        try:
            return {
                "kind": "task",
                "page": int(parts[2]),
                "task_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "op" and len(parts) == 3:
        try:
            return {"kind": "open", "discussion_uuid": UUID(parts[2])}
        except ValueError:
            return None

    if kind == "tg" and len(parts) == 4:
        try:
            return {
                "kind": "toggle",
                "page": int(parts[2]),
                "user_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "st" and len(parts) == 3:
        try:
            return {"kind": "start", "page": int(parts[2])}
        except ValueError:
            return None

    if kind == "pg" and len(parts) == 3:
        try:
            return {"kind": "picker_page", "page": int(parts[2])}
        except ValueError:
            return None

    if kind == "cn" and len(parts) == 2:
        return {"kind": "cancel"}

    if kind == "sp" and len(parts) == 2:
        return {"kind": "stop"}

    if kind == "ad" and len(parts) == 3:
        try:
            return {"kind": "add", "discussion_uuid": UUID(parts[2])}
        except ValueError:
            return None

    if kind == "at" and len(parts) == 5:
        try:
            return {
                "kind": "add_toggle",
                "page": int(parts[2]),
                "discussion_uuid": UUID(parts[3]),
                "user_uuid": UUID(parts[4]),
            }
        except ValueError:
            return None

    if kind == "ap" and len(parts) == 4:
        try:
            return {
                "kind": "add_page",
                "page": int(parts[2]),
                "discussion_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "ac" and len(parts) == 4:
        try:
            return {
                "kind": "add_confirm",
                "page": int(parts[2]),
                "discussion_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "ax" and len(parts) == 3:
        try:
            return {"kind": "add_cancel", "discussion_uuid": UUID(parts[2])}
        except ValueError:
            return None

    return None


def _user_label(*, user: Any) -> str:
    """Return a compact label for a studio user."""
    name = user.full_name if hasattr(user, "full_name") else user.get_full_name()
    if name:
        return name if len(name) <= 24 else f"{name[:21]}..."
    email = user.email.split("@", maxsplit=1)[0]
    return email if len(email) <= 24 else f"{email[:21]}..."


def _personal_discussion_label(*, discussion: Any, viewer: Any) -> str:
    """Return a distinguishable label for a personal discussion."""
    names: list[str] = []
    for membership in discussion.memberships.all():
        if membership.user_id == viewer.pk:
            continue
        user = membership.user
        name = user.full_name if hasattr(user, "full_name") else user.get_full_name()
        names.append(name or user.email.split("@", maxsplit=1)[0])

    if not names:
        return "💬 Личный диалог"
    if len(names) == 1:
        label = f"💬 {names[0]}"
    elif len(names) == 2:
        label = f"💬 {names[0]}, {names[1]}"
    else:
        label = f"💬 {names[0]}, {names[1]} +{len(names) - 2}"
    return label if len(label) <= 42 else f"{label[:39]}..."


def build_discussion_list_keyboard(
    *,
    discussions: list[Any],
    page: int,
    total_count: int,
    viewer: Any,
    page_size: int = DISCUSSION_PAGE_SIZE,
) -> dict[str, Any]:
    """Return inline keyboard markup for existing discussions."""
    rows: list[list[dict[str, str]]] = [
        [{"text": "➕ Новый диалог", "callback_data": build_discussion_new_callback()}]
    ]

    seen_uuids: set[str] = set()
    for discussion in discussions:
        discussion_uuid = str(discussion.uuid)
        if discussion_uuid in seen_uuids:
            continue
        seen_uuids.add(discussion_uuid)

        if discussion.task_id and getattr(discussion, "task", None):
            task = discussion.task
            project = getattr(task, "project", None)
            project_slug = project.slug if project else "без_проекта"
            label = f"💬 {project_slug} / {task.title}"
        else:
            label = _personal_discussion_label(discussion=discussion, viewer=viewer)
        if len(label) > 42:
            label = f"{label[:39]}..."
        rows.append(
            [
                {
                    "text": label,
                    "callback_data": build_discussion_open_callback(
                        discussion_uuid=discussion.uuid
                    ),
                }
            ]
        )

    nav_row: list[dict[str, str]] = []
    if page > 0:
        nav_row.append(
            {
                "text": "◀️ Назад",
                "callback_data": build_discussion_menu_callback(page=page - 1),
            }
        )
    total_pages = max(1, ceil(total_count / page_size))
    if page + 1 < total_pages:
        nav_row.append(
            {
                "text": "Вперёд ▶️",
                "callback_data": build_discussion_menu_callback(page=page + 1),
            }
        )
    if nav_row:
        rows.append(nav_row)

    return {"inline_keyboard": rows}


def build_partner_picker_keyboard(
    *,
    partners: list[Any],
    selected_user_uuids: set[str],
    page: int,
    total_count: int,
    page_size: int = PARTNER_PAGE_SIZE,
) -> dict[str, Any]:
    """Return inline keyboard for selecting discussion participants."""
    rows: list[list[dict[str, str]]] = []
    for partner in partners:
        marker = "✅" if str(partner.uuid) in selected_user_uuids else "☐"
        rows.append(
            [
                {
                    "text": f"{marker} {_user_label(user=partner)}",
                    "callback_data": build_discussion_toggle_callback(
                        user_uuid=partner.uuid,
                        page=page,
                    ),
                }
            ]
        )

    selected_count = len(selected_user_uuids)
    rows.append(
        [
            {
                "text": f"✅ Начать ({selected_count})",
                "callback_data": build_discussion_start_callback(page=page),
            },
            {"text": "❌ Отмена", "callback_data": build_discussion_cancel_callback()},
        ]
    )

    nav_row: list[dict[str, str]] = []
    if page > 0:
        nav_row.append(
            {
                "text": "◀️ Назад",
                "callback_data": build_discussion_picker_page_callback(page=page - 1),
            }
        )
    total_pages = max(1, ceil(total_count / page_size))
    if page + 1 < total_pages:
        nav_row.append(
            {
                "text": "Вперёд ▶️",
                "callback_data": build_discussion_picker_page_callback(page=page + 1),
            }
        )
    if nav_row:
        rows.append(nav_row)

    return {"inline_keyboard": rows}


def build_active_discussion_reply_keyboard(*, input_placeholder: str) -> dict[str, Any]:
    """Return reply keyboard and input hint for an active discussion."""
    placeholder = input_placeholder[:64]
    return {
        "keyboard": [[{"text": DISCUSSION_STOP_BUTTON}]],
        "resize_keyboard": True,
        "is_persistent": True,
        "input_field_placeholder": placeholder,
    }


def build_active_discussion_keyboard(*, discussion_uuid: UUID) -> dict[str, Any]:
    """Return inline keyboard shown while a discussion is active."""
    return {
        "inline_keyboard": [
            [
                {
                    "text": "➕ Добавить участника",
                    "callback_data": build_discussion_add_callback(
                        discussion_uuid=discussion_uuid
                    ),
                }
            ],
            [
                {
                    "text": DISCUSSION_STOP_BUTTON,
                    "callback_data": build_discussion_stop_callback(),
                }
            ],
        ]
    }


def build_add_participant_keyboard(
    *,
    partners: list[Any],
    selected_user_uuids: set[str],
    page: int,
    total_count: int,
    discussion_uuid: UUID,
    page_size: int = PARTNER_PAGE_SIZE,
) -> dict[str, Any]:
    """Return inline keyboard for adding participants to an existing discussion."""
    rows: list[list[dict[str, str]]] = []
    for partner in partners:
        marker = "✅" if str(partner.uuid) in selected_user_uuids else "☐"
        rows.append(
            [
                {
                    "text": f"{marker} {_user_label(user=partner)}",
                    "callback_data": build_discussion_add_toggle_callback(
                        discussion_uuid=discussion_uuid,
                        user_uuid=partner.uuid,
                        page=page,
                    ),
                }
            ]
        )

    selected_count = len(selected_user_uuids)
    rows.append(
        [
            {
                "text": f"✅ Добавить ({selected_count})",
                "callback_data": build_discussion_add_confirm_callback(
                    discussion_uuid=discussion_uuid,
                    page=page,
                ),
            },
            {
                "text": "❌ Отмена",
                "callback_data": build_discussion_add_cancel_callback(
                    discussion_uuid=discussion_uuid
                ),
            },
        ]
    )

    nav_row: list[dict[str, str]] = []
    if page > 0:
        nav_row.append(
            {
                "text": "◀️ Назад",
                "callback_data": build_discussion_add_page_callback(
                    discussion_uuid=discussion_uuid,
                    page=page - 1,
                ),
            }
        )
    total_pages = max(1, ceil(total_count / page_size))
    if page + 1 < total_pages:
        nav_row.append(
            {
                "text": "Вперёд ▶️",
                "callback_data": build_discussion_add_page_callback(
                    discussion_uuid=discussion_uuid,
                    page=page + 1,
                ),
            }
        )
    if nav_row:
        rows.append(nav_row)

    return {"inline_keyboard": rows}
