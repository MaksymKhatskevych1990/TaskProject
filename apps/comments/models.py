"""Discussion models."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Discussion(BaseModel):
    """Conversation between studio users, optionally linked to a task."""

    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="discussions",
        verbose_name=_("задача"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_discussions",
        verbose_name=_("создал"),
    )
    is_active = models.BooleanField(_("активен"), default=True, db_index=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = _("обсуждение")
        verbose_name_plural = _("обсуждения")

    def __str__(self) -> str:
        if self.task_id:
            return f"Discussion<{self.task.title}>"
        return f"Discussion<{self.uuid}>"


class DiscussionParticipant(BaseModel):
    """Membership of a user in a discussion."""

    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name=_("обсуждение"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discussion_memberships",
        verbose_name=_("участник"),
    )

    class Meta:
        ordering = ["user__email"]
        verbose_name = _("участник обсуждения")
        verbose_name_plural = _("участники обсуждения")
        constraints = [
            models.UniqueConstraint(
                fields=("discussion", "user"),
                name="comments_unique_discussion_participant",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.email} in {self.discussion_id}"


class DiscussionMessage(BaseModel):
    """Single message posted inside a discussion."""

    class Source(models.TextChoices):
        TELEGRAM = "telegram", _("Telegram")
        WEB = "web", _("Web")

    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("обсуждение"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discussion_messages",
        verbose_name=_("автор"),
    )
    body = models.TextField(_("сообщение"))
    source = models.CharField(
        _("источник"),
        max_length=20,
        choices=Source.choices,
        default=Source.TELEGRAM,
        db_index=True,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("сообщение обсуждения")
        verbose_name_plural = _("сообщения обсуждения")

    def __str__(self) -> str:
        preview = self.body if len(self.body) <= 40 else f"{self.body[:37]}..."
        return f"{self.author.email}: {preview}"
