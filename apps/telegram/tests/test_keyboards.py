"""Telegram keyboard tests."""

from django.test import SimpleTestCase

from apps.tasks.choices import TaskStatus
from apps.telegram.keyboards import (
    build_task_callback_data,
    build_task_keyboard,
    parse_task_callback_data,
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
