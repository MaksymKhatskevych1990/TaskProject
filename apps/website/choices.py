"""Choices for website models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class BlogPostStatus(models.TextChoices):
    """Publication state for blog posts."""

    DRAFT = "draft", _("черновик")
    PUBLISHED = "published", _("опубликовано")


class PortfolioAccent(models.TextChoices):
    """Accent color for portfolio cards."""

    CYAN = "cyan", _("cyan")
    VIOLET = "violet", _("violet")
    GREEN = "green", _("green")
    ORANGE = "orange", _("orange")
