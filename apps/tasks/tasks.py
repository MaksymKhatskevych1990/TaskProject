"""Celery tasks for task reminders."""

import logging
from itertools import groupby

from celery import shared_task
from django.conf import settings

from apps.tasks.reminders import (
    format_daily_reminder_message,
    list_tasks_with_upcoming_deadlines,
)
from apps.telegram.services import queue_telegram_message

logger = logging.getLogger(__name__)


@shared_task(name="apps.tasks.tasks.send_daily_deadline_reminders")
def send_daily_deadline_reminders() -> int:
    """Send one Telegram reminder per assignee with open tasks that have due dates."""
    if not settings.TELEGRAM_ENABLED:
        logger.info("Skipped daily deadline reminders because Telegram is disabled")
        return 0

    queryset = list_tasks_with_upcoming_deadlines()
    sent_count = 0

    for _assignee_id, tasks_iter in groupby(queryset, key=lambda task: task.assignee_id):
        tasks = list(tasks_iter)
        assignee = tasks[0].assignee
        account = getattr(assignee, "telegram_account", None)
        if account is None or not account.is_ready_for_notifications:
            continue

        text = format_daily_reminder_message(tasks=tasks)
        queue_telegram_message(chat_id=account.chat_id, text=text)
        sent_count += 1
        logger.info(
            "Queued daily deadline reminder",
            extra={
                "assignee_uuid": str(assignee.uuid),
                "task_count": len(tasks),
            },
        )

    return sent_count
