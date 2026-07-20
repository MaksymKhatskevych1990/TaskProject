"""Telegram signal adapters."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.telegram.services import ensure_telegram_account

User = get_user_model()


@receiver(post_save, sender=User)
def create_telegram_account_for_new_user(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: object,
) -> None:
    """Ensure every user has a Telegram account placeholder after creation."""
    if created:
        ensure_telegram_account(user=instance)
