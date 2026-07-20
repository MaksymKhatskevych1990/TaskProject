"""Telegram integration models."""

import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class TelegramAccount(BaseModel):
    """Telegram contact linked to a studio user for task notifications."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="telegram_account",
        verbose_name=_("пользователь"),
    )
    username = models.CharField(
        _("Telegram username"),
        max_length=64,
        blank=True,
        help_text=_("Без символа @, например: ivan_petrov"),
    )
    chat_id = models.BigIntegerField(
        _("Telegram chat ID"),
        blank=True,
        null=True,
        db_index=True,
        help_text=_("Числовой ID чата для отправки задач ботом"),
    )
    notifications_enabled = models.BooleanField(
        _("уведомления включены"),
        default=True,
    )
    link_token = models.UUIDField(
        _("токен привязки"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        ordering = ["user__email"]
        verbose_name = _("Telegram аккаунт")
        verbose_name_plural = _("Telegram аккаунты")

    def __str__(self) -> str:
        label = self.username or self.chat_id or "—"
        return f"Telegram<{self.user.email}: {label}>"

    @property
    def is_ready_for_notifications(self) -> bool:
        """Return whether the bot can send messages to this user."""
        return bool(self.notifications_enabled and self.chat_id)

    @property
    def bot_link(self) -> str:
        """Return a deep link that binds this account to a Telegram chat."""
        from apps.telegram.client import build_bot_deeplink

        bot_username = getattr(settings, "TELEGRAM_BOT_USERNAME", "")
        if not bot_username:
            return ""
        return build_bot_deeplink(start_parameter=str(self.link_token))
