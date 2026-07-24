"""Telegram keyboard tests."""

from uuid import UUID

from django.test import SimpleTestCase

from apps.tasks.choices import TaskStatus
from apps.telegram.keyboards import (
    HISTORY_PAGE_SIZE,
    MENU_TASKS_BUTTON,
    UNASSIGNED_PROJECT_TOKEN,
    build_history_action_callback,
    build_history_project_tasks_callback,
    build_history_projects_callback,
    build_history_view_callback,
    build_main_menu_keyboard,
    build_project_history_keyboard,
    build_task_callback_data,
    build_task_detail_keyboard,
    build_task_history_keyboard,
    build_task_keyboard,
    parse_history_callback,
    parse_task_callback_data,
    project_label,
)


class TaskKeyboardTests(SimpleTestCase):
    """Verify inline keyboard markup for task notifications."""

    def test_build_keyboard_for_new_task(self) -> None:
        """New tasks expose both action buttons."""
        task = type(
            "TaskStub",
            (),
            {"uuid": "11111111-1111-1111-1111-111111111111", "status": TaskStatus.TODO},
        )()

        keyboard = build_task_keyboard(task)

        self.assertIsNotNone(keyboard)
        labels = [button["text"] for row in keyboard["inline_keyboard"] for button in row]
        self.assertEqual(labels, ["▶️ В работе", "✅ Готово"])

    def test_build_keyboard_for_in_progress_task(self) -> None:
        """In-progress tasks expose only the done button."""
        task = type(
            "TaskStub",
            (),
            {
                "uuid": "11111111-1111-1111-1111-111111111111",
                "status": TaskStatus.IN_PROGRESS,
            },
        )()

        keyboard = build_task_keyboard(task)

        self.assertIsNotNone(keyboard)
        labels = [button["text"] for row in keyboard["inline_keyboard"] for button in row]
        self.assertEqual(labels, ["✅ Готово"])

    def test_build_keyboard_for_done_task(self) -> None:
        """Completed tasks do not expose action buttons."""
        task = type(
            "TaskStub",
            (),
            {"uuid": "11111111-1111-1111-1111-111111111111", "status": TaskStatus.DONE},
        )()

        self.assertIsNone(build_task_keyboard(task))

    def test_parse_callback_data(self) -> None:
        """Callback data round-trips through the parser."""
        task_uuid = "11111111-1111-1111-1111-111111111111"
        raw = build_task_callback_data(task_uuid=task_uuid, action="done")

        parsed = parse_task_callback_data(raw)

        self.assertIsNotNone(parsed)
        self.assertEqual(str(parsed[0]), task_uuid)
        self.assertEqual(parsed[1], "done")


class HistoryKeyboardTests(SimpleTestCase):
    """Verify keyboard markup for the task history menu."""

    def test_build_main_menu_keyboard(self) -> None:
        """Main menu exposes task history and help buttons."""
        keyboard = build_main_menu_keyboard()

        labels = [button["text"] for row in keyboard["keyboard"] for button in row]
        self.assertEqual(
            labels,
            [MENU_TASKS_BUTTON, "💬 Диалоги", "ℹ️ Помощь"],
        )

    def test_build_project_history_keyboard(self) -> None:
        """Project list renders one button per project."""
        project = type(
            "ProjectStub",
            (),
            {
                "uuid": UUID("22222222-2222-2222-2222-222222222222"),
                "slug": "косметик_шоп",
                "task_count": 3,
            },
        )()

        keyboard = build_project_history_keyboard(
            projects=[project],
            page=0,
            total_count=1,
            include_unassigned=True,
            unassigned_count=2,
        )

        labels = [button["text"] for row in keyboard["inline_keyboard"] for button in row]
        self.assertEqual(labels[0], "📁 без_проекта · 2")
        self.assertEqual(labels[1], "📁 косметик_шоп · 3")

    def test_build_task_history_keyboard(self) -> None:
        """Task list renders task buttons and project navigation."""
        tasks = [
            type(
                "TaskStub",
                (),
                {
                    "uuid": UUID("11111111-1111-1111-1111-111111111111"),
                    "title": "Task 1",
                    "status": TaskStatus.TODO,
                },
            )(),
        ]
        project_uuid = UUID("22222222-2222-2222-2222-222222222222")

        keyboard = build_task_history_keyboard(
            tasks=tasks,
            page=1,
            total_count=HISTORY_PAGE_SIZE + 1,
            project_uuid=project_uuid,
        )

        labels = [button["text"] for row in keyboard["inline_keyboard"] for button in row]
        self.assertEqual(labels[0], "⏳ Task 1")
        self.assertIn("◀️ К проектам", labels)
        self.assertIn("◀️ Назад", labels)
        self.assertNotIn("Вперёд ▶️", labels)

    def test_build_task_detail_keyboard(self) -> None:
        """Task detail includes back navigation and status actions."""
        project = type(
            "ProjectStub",
            (),
            {"uuid": UUID("22222222-2222-2222-2222-222222222222"), "slug": "косметик_шоп"},
        )()
        task = type(
            "TaskStub",
            (),
            {
                "uuid": UUID("11111111-1111-1111-1111-111111111111"),
                "status": TaskStatus.TODO,
                "project": project,
            },
        )()

        keyboard = build_task_detail_keyboard(task=task, page=2)
        labels = [button["text"] for row in keyboard["inline_keyboard"] for button in row]

        self.assertEqual(labels[0], "◀️ К задачам")
        self.assertIn("📎 Файлы", labels)
        self.assertIn("💬 Обсудить", labels)
        self.assertIn("▶️ В работе", labels)
        self.assertIn("✅ Готово", labels)

    def test_parse_history_callbacks(self) -> None:
        """History callback data round-trips through the parser."""
        task_uuid = UUID("11111111-1111-1111-1111-111111111111")
        project_uuid = UUID("22222222-2222-2222-2222-222222222222")

        self.assertEqual(
            parse_history_callback(build_history_projects_callback(page=2)),
            {"kind": "projects", "page": 2},
        )
        self.assertEqual(
            parse_history_callback(
                build_history_project_tasks_callback(project_uuid=project_uuid, page=1)
            ),
            {"kind": "project_tasks", "page": 1, "project_uuid": project_uuid},
        )
        self.assertEqual(
            parse_history_callback(
                build_history_project_tasks_callback(project_uuid=None, page=0)
            ),
            {"kind": "project_tasks", "page": 0, "project_uuid": None},
        )
        self.assertEqual(
            parse_history_callback(build_history_view_callback(page=1, task_uuid=task_uuid)),
            {"kind": "view", "page": 1, "task_uuid": task_uuid},
        )
        self.assertEqual(
            parse_history_callback(
                build_history_action_callback(
                    task_uuid=task_uuid,
                    page=0,
                    action="done",
                )
            ),
            {
                "kind": "action",
                "page": 0,
                "task_uuid": task_uuid,
                "action": "done",
            },
        )
        self.assertEqual(project_label(project=None), "без_проекта")
        self.assertEqual(project_label(project=type("P", (), {"slug": "косметик_шоп"})()), "косметик_шоп")
