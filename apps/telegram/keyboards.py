"""Telegram inline keyboard builders."""

from typing import Any
from uuid import UUID

from apps.tasks.choices import TaskStatus


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
