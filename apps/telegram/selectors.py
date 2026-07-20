"""Telegram read operations."""

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.telegram.models import TelegramAccount

User = get_user_model()


def get_telegram_account_for_user(*, user: User) -> TelegramAccount | None:
    """Return the Telegram account linked to a user, if any."""
    return TelegramAccount.objects.filter(user=user).first()


def list_notification_ready_accounts() -> QuerySet[TelegramAccount]:
    """Return accounts that can receive Telegram task notifications."""
    return TelegramAccount.objects.filter(
        notifications_enabled=True,
        chat_id__isnull=False,
        user__is_active=True,
    ).select_related("user")
