"""Employee, team, and position models."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Position(BaseModel):
    """Catalog entry for a studio job title."""

    title = models.CharField(_("название"), max_length=120, unique=True)
    is_active = models.BooleanField(_("активна"), default=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("должность")
        verbose_name_plural = _("должности")

    def __str__(self) -> str:
        return self.title


class Team(BaseModel):
    """Working group of studio members."""

    name = models.CharField(_("название"), max_length=120, unique=True)
    description = models.TextField(_("описание"), blank=True)
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="led_teams",
        verbose_name=_("руководитель"),
    )
    is_active = models.BooleanField(_("активна"), default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("команда")
        verbose_name_plural = _("команды")

    def __str__(self) -> str:
        return self.name


class Employee(BaseModel):
    """Organizational record linking a user to team and position."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name=_("пользователь"),
    )
    team = models.ForeignKey(
        Team,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="members",
        verbose_name=_("команда"),
    )
    position = models.ForeignKey(
        Position,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="employees",
        verbose_name=_("должность"),
    )
    hire_date = models.DateField(_("дата найма"), blank=True, null=True)
    notes = models.TextField(_("заметки"), blank=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name", "user__email"]
        verbose_name = _("сотрудник")
        verbose_name_plural = _("сотрудники")

    def __str__(self) -> str:
        return f"Employee<{self.user.email}>"
