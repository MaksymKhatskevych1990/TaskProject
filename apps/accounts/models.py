"""Account and profile models."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.choices import UserRole
from apps.accounts.managers import UserManager
from apps.common.models import BaseModel


class User(AbstractUser):
    """Internal studio user authenticated by email."""

    username = None
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("адрес электронной почты"), unique=True)
    role = models.CharField(
        _("роль"),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EMPLOYEE,
        db_index=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        """Return the user's display name."""
        return self.get_full_name().strip() or self.email

    @property
    def is_admin(self) -> bool:
        """Return whether the user has administrative privileges."""
        return self.is_superuser or self.role == UserRole.ADMIN

    @property
    def is_manager(self) -> bool:
        """Return whether the user can act as a manager."""
        return self.is_admin or self.role == UserRole.MANAGER

    @property
    def is_employee(self) -> bool:
        """Return whether the user is an active studio member."""
        return self.is_active


class Profile(BaseModel):
    """Extended user information managed separately from authentication."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("пользователь"),
    )
    phone = models.CharField(_("телефон"), max_length=32, blank=True)
    position = models.CharField(_("должность"), max_length=120, blank=True)
    bio = models.TextField(_("о себе"), blank=True)
    timezone = models.CharField(_("часовой пояс"), max_length=64, default="Europe/Kyiv")
    avatar = models.ImageField(_("аватар"), upload_to="avatars/", blank=True)

    class Meta:
        ordering = ["user__email"]
        verbose_name = _("профиль")
        verbose_name_plural = _("профили")

    def __str__(self) -> str:
        return f"Profile<{self.user.email}>"
