"""Reusable SEO fields that actually affect search snippets."""

from django.db import models
from django.utils.translation import gettext_lazy as _


def seo_og_upload_to(instance, filename: str) -> str:
    """Store Open Graph images under a stable per-object path."""
    model = instance._meta.model_name
    ident = getattr(instance, "slug", None) or getattr(instance, "pk", "draft")
    return f"seo/{model}/{ident}/{filename}"


class SeoFieldsMixin(models.Model):
    """Title, snippet, social preview, and indexation controls."""

    SEO_FIELDS = (
        "focus_keyword",
        "seo_title",
        "seo_description",
        "seo_h1",
        "og_title",
        "og_description",
        "og_image",
        "canonical_url",
        "robots_noindex",
        "secondary_keywords",
    )

    focus_keyword = models.CharField(
        _("ключевой запрос"),
        max_length=80,
        blank=True,
        help_text=_(
            "Один основной запрос, не список. Он должен быть в title, H1 и первом абзаце."
        ),
    )
    seo_title = models.CharField(
        _("Title"),
        max_length=70,
        blank=True,
        help_text=_(
            "50–60 символов. Заголовок в Google. Если пусто — возьмём название страницы."
        ),
    )
    seo_description = models.CharField(
        _("Meta description"),
        max_length=180,
        blank=True,
        help_text=_(
            "140–160 символов. Текст под заголовком в поиске: запрос, польза и призыв."
        ),
    )
    seo_h1 = models.CharField(
        _("H1"),
        max_length=150,
        blank=True,
        help_text=_(
            "Главный заголовок на странице. Если пусто — покажем обычное название."
        ),
    )
    og_title = models.CharField(
        _("Open Graph title"),
        max_length=70,
        blank=True,
        help_text=_(
            "Заголовок для Telegram, Facebook и LinkedIn. Если пусто — возьмём Title."
        ),
    )
    og_description = models.CharField(
        _("Open Graph description"),
        max_length=180,
        blank=True,
        help_text=_("Текст превью в соцсетях. Если пусто — возьмём meta description."),
    )
    og_image = models.ImageField(
        _("Open Graph изображение"),
        upload_to=seo_og_upload_to,
        blank=True,
        help_text=_(
            "1200×630 px. Без него соцсети возьмут обложку или картинку по умолчанию."
        ),
    )
    canonical_url = models.URLField(
        _("Canonical URL"),
        blank=True,
        help_text=_(
            "Только если страница дублирует другую. Иначе оставьте пустым — подставим автоматически."
        ),
    )
    robots_noindex = models.BooleanField(
        _("скрыть от Google (noindex)"),
        default=False,
        help_text=_(
            "Включайте для черновиков, служебных и дублей. Не включайте на страницах для трафика."
        ),
    )
    secondary_keywords = models.CharField(
        _("дополнительные запросы"),
        max_length=250,
        blank=True,
        help_text=_(
            "Через запятую, для текста страницы. Не выводим как meta keywords — Google их игнорирует."
        ),
    )

    class Meta:
        abstract = True

    def resolve_seo_title(self, fallback: str) -> str:
        """Return the title tag, falling back to the page name."""
        return (self.seo_title or "").strip() or fallback

    def resolve_seo_description(self, fallback: str) -> str:
        """Return the meta description, falling back to the page summary."""
        return (self.seo_description or "").strip() or fallback

    def resolve_h1(self, fallback: str) -> str:
        """Return the visible H1, falling back to the page name."""
        return (self.seo_h1 or "").strip() or fallback

    def resolve_og_title(self, fallback: str) -> str:
        """Return the social title, falling back to the SEO title."""
        return (self.og_title or "").strip() or self.resolve_seo_title(fallback)

    def resolve_og_description(self, fallback: str) -> str:
        """Return the social description, falling back to the meta description."""
        return (self.og_description or "").strip() or self.resolve_seo_description(
            fallback
        )

    def seo_is_complete(self) -> bool:
        """Return whether the two fields that form the Google snippet are filled."""
        return bool(
            (self.seo_title or "").strip() and (self.seo_description or "").strip()
        )
