"""Project models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Project(BaseModel):
    """Studio project that groups related tasks."""

    name = models.CharField(_("название"), max_length=200)
    slug = models.SlugField(
        _("slug"),
        max_length=100,
        unique=True,
        allow_unicode=True,
        help_text=_("Короткий идентификатор, например: косметик_шоп"),
    )
    is_active = models.BooleanField(_("активен"), default=True, db_index=True)

    class Meta:
        ordering = ["slug"]
        verbose_name = _("проект")
        verbose_name_plural = _("проекты")

    def __str__(self) -> str:
        return self.slug
