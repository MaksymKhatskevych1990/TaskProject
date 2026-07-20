"""Account signal adapters."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.accounts.services import ensure_user_profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: object,
) -> None:
    """Ensure every user has a profile after creation."""
    if created:
        ensure_user_profile(user=instance)
