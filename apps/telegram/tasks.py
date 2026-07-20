"""Celery tasks for Telegram delivery."""

import logging

from celery import shared_task

from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.services import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(TelegramAPIError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_telegram_message_task(self, chat_id: int, text: str) -> bool:
    """Deliver a Telegram message asynchronously."""
    try:
        return send_telegram_message(chat_id=chat_id, text=text)
    except TelegramDisabledError:
        logger.info(
            "Skipped async Telegram message because integration is disabled",
            extra={"chat_id": chat_id},
        )
        return False
