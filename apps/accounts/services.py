"""Account business operations."""

import logging
from typing import Any

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import selectors
from apps.accounts.choices import UserRole
from apps.accounts.models import Profile, User
from apps.telegram import services as telegram_services
from apps.telegram.services import TELEGRAM_FIELDS

logger = logging.getLogger(__name__)

USER_FIELDS = {"first_name", "last_name", "role", "is_active"}
PROFILE_FIELDS = {"phone", "position", "bio", "timezone", "avatar"}


def ensure_user_profile(*, user: User) -> Profile:
    """Create a profile when one does not exist yet."""
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        logger.info("Created profile for user", extra={"user_uuid": str(user.uuid)})
    return profile


def create_user(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: str = UserRole.EMPLOYEE,
    actor: User | None = None,
    profile_data: dict[str, Any] | None = None,
    telegram_data: dict[str, Any] | None = None,
) -> User:
    """Create a user and the associated profile."""
    if selectors.get_user_by_email(email):
        raise ValidationError({"email": ["A user with this email already exists."]})

    profile_data = profile_data or {}
    with transaction.atomic():
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        profile = selectors.get_user_profile(user)
        for field in PROFILE_FIELDS:
            if field in profile_data:
                setattr(profile, field, profile_data[field])
        if actor is not None:
            profile.created_by = actor
        profile.save()
        if telegram_data:
            telegram_services.update_telegram_account(
                user=user,
                data=telegram_data,
                actor=actor,
            )
    logger.info("Created user", extra={"user_uuid": str(user.uuid), "role": role})
    return selectors.get_user_with_profile(user)


def update_user(
    *,
    user: User,
    data: dict[str, Any],
    actor: User,
) -> User:
    """Update user fields and keep administrative flags in sync."""
    user_updates = {key: data[key] for key in USER_FIELDS if key in data}
    profile_updates = {key: data[key] for key in PROFILE_FIELDS if key in data}
    telegram_updates = {key: data[key] for key in TELEGRAM_FIELDS if key in data}

    with transaction.atomic():
        if user_updates:
            for field, value in user_updates.items():
                setattr(user, field, value)
            if "role" in user_updates:
                user.is_staff = user.role == UserRole.ADMIN or user.is_superuser
            user.save()
            user.refresh_from_db()

        if profile_updates:
            profile = selectors.get_user_profile(user)
            for field, value in profile_updates.items():
                setattr(profile, field, value)
            profile.updated_by = actor
            profile.save()

        if telegram_updates:
            telegram_services.update_telegram_account(
                user=user,
                data=telegram_updates,
                actor=actor,
            )

    logger.info("Updated user", extra={"user_uuid": str(user.uuid)})
    return selectors.get_user_with_profile(user)


def update_me(*, user: User, data: dict[str, Any]) -> User:
    """Update the authenticated user's own account data."""
    allowed_fields = {"first_name", "last_name", *PROFILE_FIELDS}
    return update_user(
        user=user,
        data={key: value for key, value in data.items() if key in allowed_fields},
        actor=user,
    )


def change_password(*, user: User, current_password: str, new_password: str) -> None:
    """Change the password for an authenticated user."""
    if not user.check_password(current_password):
        raise ValidationError({"current_password": ["Current password is incorrect."]})
    user.set_password(new_password)
    user.save(update_fields=["password"])
    logger.info("Changed password", extra={"user_uuid": str(user.uuid)})


def deactivate_user(*, user: User, actor: User) -> User:
    """Deactivate a user account without deleting history."""
    if user.pk == actor.pk:
        raise ValidationError({"detail": ["You cannot deactivate your own account."]})

    user.is_active = False
    user.save(update_fields=["is_active"])
    logger.info(
        "Deactivated user",
        extra={"user_uuid": str(user.uuid), "actor_uuid": str(actor.uuid)},
    )
    return selectors.get_user_with_profile(user)


def logout_user(*, refresh_token: str) -> None:
    """Blacklist a refresh token."""
    try:
        token = RefreshToken(refresh_token)
    except Exception as exc:
        raise ValidationError({"refresh": ["Invalid refresh token."]}) from exc
    token.blacklist()
