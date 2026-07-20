"""Read-only account queries."""

from uuid import UUID

from django.db.models import QuerySet

from apps.accounts.models import Profile, User


def get_user_by_email(email: str) -> User | None:
    """Return a user by email address."""
    return User.objects.filter(email__iexact=email).first()


def get_user_by_uuid(user_uuid: UUID) -> User:
    """Return a user with profile data preloaded."""
    return User.objects.select_related("profile", "telegram_account").get(uuid=user_uuid)


def get_user_with_profile(user: User) -> User:
    """Return the user with profile data preloaded."""
    return User.objects.select_related("profile", "telegram_account").get(pk=user.pk)


def get_user_profile(user: User) -> Profile:
    """Return the profile for the given user."""
    return Profile.objects.select_related("user").get(user=user)


def list_users(
    *,
    is_active: bool | None = None,
    role: str | None = None,
) -> QuerySet[User]:
    """Return users ordered by newest first."""
    queryset = User.objects.select_related("profile", "telegram_account").order_by(
        "-date_joined"
    )
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    if role:
        queryset = queryset.filter(role=role)
    return queryset
