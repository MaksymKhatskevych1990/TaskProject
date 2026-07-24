"""Discussion application configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    """Configure the comments application boundary."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comments"
    verbose_name = _("Обсуждения")
