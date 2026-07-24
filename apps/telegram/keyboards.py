"""Telegram keyboard builders."""

from math import ceil
from typing import Any
from uuid import UUID

from apps.tasks.choices import TaskStatus

from apps.telegram.discussion_keyboards import build_discussion_task_callback

MENU_TASKS_BUTTON = "📋 Мои задачи"
MENU_HELP_BUTTON = "ℹ️ Помощь"

HISTORY_PAGE_SIZE = 5
UNASSIGNED_PROJECT_TOKEN = "none"

STATUS_EMOJI = {
    TaskStatus.TODO: "⏳",
    TaskStatus.IN_PROGRESS: "🔄",
    TaskStatus.DONE: "✅",
    TaskStatus.CANCELLED: "❌",
}


def build_main_menu_keyboard() -> dict[str, Any]:
    """Return the persistent reply keyboard shown after account linking."""
    from apps.telegram.discussion_keyboards import MENU_DIALOGS_BUTTON

    return {
        "keyboard": [
            [{"text": MENU_TASKS_BUTTON}],
            [{"text": MENU_DIALOGS_BUTTON}, {"text": MENU_HELP_BUTTON}],
        ],
        "resize_keyboard": True,
        "is_persistent": True,
    }


def build_task_callback_data(*, task_uuid: UUID, action: str) -> str:
    """Build compact callback data for a task action button."""
    return f"task:{task_uuid}:{action}"


def parse_task_callback_data(data: str) -> tuple[UUID, str] | None:
    """Parse callback data emitted by task notification buttons."""
    parts = data.split(":", 2)
    if len(parts) != 3 or parts[0] != "task":
        return None
    try:
        task_uuid = UUID(parts[1])
    except ValueError:
        return None
    return task_uuid, parts[2]


def _project_token(*, project_uuid: UUID | None) -> str:
    """Encode a project UUID for compact callback data."""
    return str(project_uuid) if project_uuid is not None else UNASSIGNED_PROJECT_TOKEN


def _parse_project_token(token: str) -> UUID | None:
    """Decode a project token from callback data."""
    if token == UNASSIGNED_PROJECT_TOKEN:
        return None
    return UUID(token)


def build_history_projects_callback(*, page: int) -> str:
    """Build callback data for a paginated project list."""
    return f"hist:pr:{page}"


def build_history_project_tasks_callback(*, project_uuid: UUID | None, page: int) -> str:
    """Build callback data for a paginated task list inside a project."""
    return f"hist:pt:{page}:{_project_token(project_uuid=project_uuid)}"


def build_history_view_callback(*, page: int, task_uuid: UUID) -> str:
    """Build callback data for opening a task from the history list."""
    return f"hist:v:{page}:{task_uuid}"


def build_history_action_callback(*, task_uuid: UUID, page: int, action: str) -> str:
    """Build callback data for changing task status from the history view."""
    return f"hist:a:{page}:{task_uuid}:{action}"


def build_history_files_callback(*, task_uuid: UUID, page: int) -> str:
    """Build callback data for viewing task attachments."""
    return f"hist:fl:{page}:{task_uuid}"


def build_history_upload_callback(*, task_uuid: UUID, page: int) -> str:
    """Build callback data for entering file upload mode."""
    return f"hist:up:{page}:{task_uuid}"


def parse_history_callback(data: str) -> dict[str, Any] | None:
    """Parse callback data emitted by the task history menu."""
    parts = data.split(":")
    if len(parts) < 3 or parts[0] != "hist":
        return None

    kind = parts[1]
    if kind == "pr" and len(parts) == 3:
        try:
            return {"kind": "projects", "page": int(parts[2])}
        except ValueError:
            return None

    if kind == "pt" and len(parts) == 4:
        try:
            return {
                "kind": "project_tasks",
                "page": int(parts[2]),
                "project_uuid": _parse_project_token(parts[3]),
            }
        except ValueError:
            return None

    if kind == "v" and len(parts) == 4:
        try:
            return {
                "kind": "view",
                "page": int(parts[2]),
                "task_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "a" and len(parts) == 5:
        try:
            return {
                "kind": "action",
                "page": int(parts[2]),
                "task_uuid": UUID(parts[3]),
                "action": parts[4],
            }
        except ValueError:
            return None

    if kind == "fl" and len(parts) == 4:
        try:
            return {
                "kind": "files",
                "page": int(parts[2]),
                "task_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    if kind == "up" and len(parts) == 4:
        try:
            return {
                "kind": "upload",
                "page": int(parts[2]),
                "task_uuid": UUID(parts[3]),
            }
        except ValueError:
            return None

    return None


def build_task_keyboard(task: Any) -> dict[str, Any] | None:
    """Return inline keyboard markup for a task notification."""
    if task.status in {TaskStatus.DONE, TaskStatus.CANCELLED}:
        return None

    rows: list[list[dict[str, str]]] = []
    if task.status == TaskStatus.TODO:
        rows.append(
            [
                {
                    "text": "▶️ В работе",
                    "callback_data": build_task_callback_data(
                        task_uuid=task.uuid,
                        action="in_progress",
                    ),
                },
                {
                    "text": "✅ Готово",
                    "callback_data": build_task_callback_data(
                        task_uuid=task.uuid,
                        action="done",
                    ),
                },
            ]
        )
    elif task.status == TaskStatus.IN_PROGRESS:
        rows.append(
            [
                {
                    "text": "✅ Готово",
                    "callback_data": build_task_callback_data(
                        task_uuid=task.uuid,
                        action="done",
                    ),
                },
            ]
        )

    if not rows:
        return None
    return {"inline_keyboard": rows}


def _history_action_rows(*, task: Any, page: int) -> list[list[dict[str, str]]]:
    """Return status action buttons for the history detail view."""
    if task.status in {TaskStatus.DONE, TaskStatus.CANCELLED}:
        return []

    rows: list[list[dict[str, str]]] = []
    if task.status == TaskStatus.TODO:
        rows.append(
            [
                {
                    "text": "▶️ В работе",
                    "callback_data": build_history_action_callback(
                        task_uuid=task.uuid,
                        page=page,
                        action="in_progress",
                    ),
                },
                {
                    "text": "✅ Готово",
                    "callback_data": build_history_action_callback(
                        task_uuid=task.uuid,
                        page=page,
                        action="done",
                    ),
                },
            ]
        )
    elif task.status == TaskStatus.IN_PROGRESS:
        rows.append(
            [
                {
                    "text": "✅ Готово",
                    "callback_data": build_history_action_callback(
                        task_uuid=task.uuid,
                        page=page,
                        action="done",
                    ),
                },
            ]
        )
    return rows


def build_project_history_keyboard(
    *,
    projects: list[Any],
    page: int,
    total_count: int,
    include_unassigned: bool,
    unassigned_count: int = 0,
    page_size: int = HISTORY_PAGE_SIZE,
) -> dict[str, Any]:
    """Return inline keyboard markup for choosing a project."""
    rows: list[list[dict[str, str]]] = []

    if include_unassigned and page == 0:
        label = f"📁 без_проекта · {unassigned_count}"
        rows.append(
            [
                {
                    "text": label,
                    "callback_data": build_history_project_tasks_callback(
                        project_uuid=None,
                        page=0,
                    ),
                }
            ]
        )

    for project in projects:
        slug = project.slug if len(project.slug) <= 28 else f"{project.slug[:25]}..."
        rows.append(
            [
                {
                    "text": f"📁 {slug} · {project.task_count}",
                    "callback_data": build_history_project_tasks_callback(
                        project_uuid=project.uuid,
                        page=0,
                    ),
                }
            ]
        )

    nav_row: list[dict[str, str]] = []
    if page > 0:
        nav_row.append(
            {
                "text": "◀️ Назад",
                "callback_data": build_history_projects_callback(page=page - 1),
            }
        )
    total_pages = max(1, ceil(total_count / page_size))
    if page + 1 < total_pages:
        nav_row.append(
            {
                "text": "Вперёд ▶️",
                "callback_data": build_history_projects_callback(page=page + 1),
            }
        )
    if nav_row:
        rows.append(nav_row)

    return {"inline_keyboard": rows}


def build_task_history_keyboard(
    *,
    tasks: list[Any],
    page: int,
    total_count: int,
    project_uuid: UUID | None,
    page_size: int = HISTORY_PAGE_SIZE,
) -> dict[str, Any]:
    """Return inline keyboard markup for a paginated task list inside a project."""
    rows: list[list[dict[str, str]]] = []
    for task in tasks:
        emoji = STATUS_EMOJI.get(task.status, "📋")
        title = task.title if len(task.title) <= 40 else f"{task.title[:37]}..."
        rows.append(
            [
                {
                    "text": f"{emoji} {title}",
                    "callback_data": build_history_view_callback(
                        page=page,
                        task_uuid=task.uuid,
                    ),
                }
            ]
        )

    nav_row: list[dict[str, str]] = [
        {
            "text": "◀️ К проектам",
            "callback_data": build_history_projects_callback(page=0),
        }
    ]
    if page > 0:
        nav_row.append(
            {
                "text": "◀️ Назад",
                "callback_data": build_history_project_tasks_callback(
                    project_uuid=project_uuid,
                    page=page - 1,
                ),
            }
        )
    total_pages = max(1, ceil(total_count / page_size))
    if page + 1 < total_pages:
        nav_row.append(
            {
                "text": "Вперёд ▶️",
                "callback_data": build_history_project_tasks_callback(
                    project_uuid=project_uuid,
                    page=page + 1,
                ),
            }
        )
    rows.append(nav_row)

    return {"inline_keyboard": rows}


def build_task_detail_keyboard(*, task: Any, page: int, attachment_count: int = 0) -> dict[str, Any]:
    """Return inline keyboard markup for a single task in history."""
    project_uuid = task.project.uuid if getattr(task, "project", None) else None
    files_label = f"📎 Файлы ({attachment_count})" if attachment_count else "📎 Файлы"
    rows: list[list[dict[str, str]]] = [
        [
            {
                "text": "◀️ К задачам",
                "callback_data": build_history_project_tasks_callback(
                    project_uuid=project_uuid,
                    page=page,
                ),
            }
        ],
        [
            {
                "text": files_label,
                "callback_data": build_history_files_callback(
                    task_uuid=task.uuid,
                    page=page,
                ),
            },
            {
                "text": "💬 Обсудить",
                "callback_data": build_discussion_task_callback(
                    task_uuid=task.uuid,
                    page=page,
                ),
            },
        ],
    ]
    rows.extend(_history_action_rows(task=task, page=page))
    return {"inline_keyboard": rows}


def build_task_files_keyboard(*, task: Any, page: int) -> dict[str, Any]:
    """Return inline keyboard for the task attachments screen."""
    project_uuid = task.project.uuid if getattr(task, "project", None) else None
    return {
        "inline_keyboard": [
            [
                {
                    "text": "⬆️ Загрузить файл",
                    "callback_data": build_history_upload_callback(
                        task_uuid=task.uuid,
                        page=page,
                    ),
                }
            ],
            [
                {
                    "text": "◀️ К задаче",
                    "callback_data": build_history_view_callback(
                        page=page,
                        task_uuid=task.uuid,
                    ),
                },
                {
                    "text": "◀️ К задачам",
                    "callback_data": build_history_project_tasks_callback(
                        project_uuid=project_uuid,
                        page=page,
                    ),
                },
            ],
        ]
    }


def project_label(*, project: Any | None) -> str:
    """Return a short project label for Telegram messages."""
    if project is None:
        return "без_проекта"
    return project.slug
