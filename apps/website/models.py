"""Public website content models."""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.website.choices import BlogPostStatus, PortfolioAccent
from apps.website.text import ensure_unique_slug, is_latin_slug, latin_slugify


def portfolio_cover_upload_to(instance: "PortfolioProject", filename: str) -> str:
    """Build a storage path for portfolio cover images."""
    return f"portfolio/{instance.slug or 'draft'}/cover/{filename}"


def portfolio_gallery_upload_to(instance: "PortfolioGalleryImage", filename: str) -> str:
    """Build a storage path for portfolio gallery images."""
    slug = instance.project.slug if instance.project_id else "draft"
    return f"portfolio/{slug}/gallery/{filename}"


class BlogCategory(BaseModel):
    """Blog post category shown on the public site."""

    name = models.CharField(_("название"), max_length=100)
    slug = models.SlugField(
        _("slug"),
        max_length=100,
        unique=True,
        allow_unicode=False,
        help_text=_("Заповнюється автоматично латиницею з назви."),
    )
    ordering = models.PositiveIntegerField(_("порядок"), default=0, db_index=True)

    class Meta:
        ordering = ["ordering", "name"]
        verbose_name = _("категория блога")
        verbose_name_plural = _("категории блога")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """Generate a Latin slug from the category name when needed."""
        if self.name and (not self.slug or not is_latin_slug(self.slug)):
            base_slug = latin_slugify(self.name)
            self.slug = ensure_unique_slug(BlogCategory, base_slug, exclude_pk=self.pk)
        super().save(*args, **kwargs)


class BlogPost(BaseModel):
    """Blog article published on the marketing site."""

    title = models.CharField(_("заголовок"), max_length=300)
    slug = models.SlugField(
        _("slug"),
        max_length=200,
        unique=True,
        allow_unicode=False,
        help_text=_("Заповнюється автоматично латиницею з заголовка."),
    )
    excerpt = models.TextField(_("краткое описание"), max_length=500)
    content = models.TextField(
        _("содержание"),
        help_text=_(
            "Абзацы разделяйте пустой строкой. Заголовки — «## Заголовок». "
            "Списки — строки с «* » или «- ». Выделение — «**жирный**»."
        ),
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name=_("категория"),
    )
    status = models.CharField(
        _("статус"),
        max_length=20,
        choices=BlogPostStatus.choices,
        default=BlogPostStatus.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(_("дата публикации"), null=True, blank=True, db_index=True)
    read_time_minutes = models.PositiveSmallIntegerField(_("время чтения (мин)"), default=5)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = _("статья блога")
        verbose_name_plural = _("статьи блога")

    def __str__(self) -> str:
        return self.title

    @property
    def is_published(self) -> bool:
        """Return whether the post is visible on the public site."""
        return self.status == BlogPostStatus.PUBLISHED and self.published_at is not None

    def save(self, *args, **kwargs) -> None:
        """Set publication timestamp when a post becomes published."""
        if self.title and (not self.slug or not is_latin_slug(self.slug)):
            base_slug = latin_slugify(self.title)
            self.slug = ensure_unique_slug(BlogPost, base_slug, exclude_pk=self.pk)
        if self.content:
            self.content = self.content.replace("\r\n", "\n").replace("\r", "\n")
        if self.status == BlogPostStatus.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class PortfolioProject(BaseModel):
    """Portfolio work published on the marketing site."""

    title = models.CharField(_("название"), max_length=200)
    slug = models.SlugField(
        _("slug"),
        max_length=200,
        unique=True,
        allow_unicode=False,
        help_text=_("Заповнюється автоматично латиницею з назви."),
    )
    category = models.CharField(_("категория"), max_length=100)
    description = models.TextField(_("краткое описание"), max_length=500)
    tags = models.JSONField(_("теги"), default=list, blank=True)
    accent = models.CharField(
        _("акцент"),
        max_length=20,
        choices=PortfolioAccent.choices,
        default=PortfolioAccent.CYAN,
    )
    gradient = models.CharField(
        _("градиент"),
        max_length=120,
        blank=True,
        help_text=_("Tailwind-класи для превʼю без обкладинки, напр. from-violet/60 to-cyan/40"),
    )
    cover_image = models.ImageField(
        _("обложка"),
        upload_to=portfolio_cover_upload_to,
        blank=True,
    )
    client_url = models.URLField(_("ссылка на сайт"), blank=True)
    featured = models.BooleanField(_("избранное"), default=False, db_index=True)
    sort_order = models.PositiveIntegerField(_("порядок"), default=0, db_index=True)
    status = models.CharField(
        _("статус"),
        max_length=20,
        choices=BlogPostStatus.choices,
        default=BlogPostStatus.DRAFT,
        db_index=True,
    )
    metric = models.CharField(_("метрика"), max_length=50, blank=True)
    before_label = models.CharField(_("было"), max_length=120, blank=True)
    after_label = models.CharField(_("стало"), max_length=120, blank=True)
    case_description = models.TextField(_("описание кейса"), max_length=2000, blank=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = _("работа портфолио")
        verbose_name_plural = _("работы портфолио")

    def __str__(self) -> str:
        return self.title

    @property
    def is_published(self) -> bool:
        """Return whether the project is visible on the public site."""
        return self.status == BlogPostStatus.PUBLISHED

    def save(self, *args, **kwargs) -> None:
        """Generate slug and default gradient when needed."""
        if self.title and (not self.slug or not is_latin_slug(self.slug)):
            base_slug = latin_slugify(self.title)
            self.slug = ensure_unique_slug(PortfolioProject, base_slug, exclude_pk=self.pk)
        if not self.gradient:
            self.gradient = self._default_gradient()
        super().save(*args, **kwargs)

    def _default_gradient(self) -> str:
        """Return a Tailwind gradient fallback for the selected accent."""
        defaults = {
            PortfolioAccent.CYAN: "from-cyan/50 to-blue-500/30",
            PortfolioAccent.VIOLET: "from-violet/60 to-cyan/40",
            PortfolioAccent.GREEN: "from-emerald-500/40 to-cyan/30",
            PortfolioAccent.ORANGE: "from-orange-500/40 to-amber-500/30",
        }
        return defaults.get(self.accent, defaults[PortfolioAccent.CYAN])


class PortfolioGalleryImage(BaseModel):
    """Additional screenshots for a portfolio case study."""

    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        verbose_name=_("проект"),
    )
    image = models.ImageField(_("изображение"), upload_to=portfolio_gallery_upload_to)
    caption = models.CharField(_("подпись"), max_length=200, blank=True)
    ordering = models.PositiveIntegerField(_("порядок"), default=0, db_index=True)

    class Meta:
        ordering = ["ordering", "created_at"]
        verbose_name = _("изображение галереи")
        verbose_name_plural = _("изображения галереи")

    def __str__(self) -> str:
        return self.caption or f"{self.project.title} #{self.ordering}"


class ContactLead(BaseModel):
    """Contact form submission from the landing page."""

    name = models.CharField(_("имя"), max_length=120)
    phone = models.CharField(_("контакт"), max_length=120)
    project = models.TextField(_("описание проекта"), max_length=2000)
    plan = models.CharField(_("тариф"), max_length=50, blank=True)
    is_processed = models.BooleanField(_("обработана"), default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("заявка с сайта")
        verbose_name_plural = _("заявки с сайта")

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"
