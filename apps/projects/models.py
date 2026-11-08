"""Project models."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.seo import SeoFieldsMixin
from apps.projects.choices import ProjectStatus


def normalize_host(value: str) -> str:
    """Store domains without a scheme or trailing path."""
    cleaned = value.strip()
    lowered = cleaned.lower()
    for prefix in ("https://", "http://"):
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix) :]
            break
    return cleaned.split("/", maxsplit=1)[0].strip()


class Project(SeoFieldsMixin, BaseModel):
    """Studio project that groups related tasks."""

    SECRET_FIELDS = (
        "server_host",
        "server_port",
        "server_username",
        "server_password",
        "server_ssh_key",
        "server_path",
        "extra_credentials",
    )

    name = models.CharField(_("название"), max_length=200)
    slug = models.SlugField(
        _("slug"),
        max_length=100,
        unique=True,
        allow_unicode=True,
        help_text=_("Короткий идентификатор, например: косметик_шоп"),
    )
    is_active = models.BooleanField(_("активен"), default=True, db_index=True)
    status = models.CharField(
        _("статус"),
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.DEVELOPMENT,
        db_index=True,
    )
    description = models.TextField(_("описание"), blank=True)
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="led_projects",
        verbose_name=_("ответственный"),
    )
    started_on = models.DateField(_("старт проекта"), blank=True, null=True)
    hosting_provider = models.CharField(
        _("хостинг"),
        max_length=120,
        blank=True,
        help_text=_("Например: Hetzner, Timeweb, Beget"),
    )
    domain = models.CharField(
        _("домен"),
        max_length=255,
        blank=True,
        help_text=_("Рабочий домен, например example.com"),
    )
    staging_domain = models.CharField(
        _("staging-домен"),
        max_length=255,
        blank=True,
        help_text=_("Тестовый адрес, если он отличается от рабочего"),
    )
    repository_url = models.CharField(
        _("репозиторий"),
        max_length=500,
        blank=True,
        help_text=_("Ссылка на GitHub, GitLab или другой репозиторий"),
    )
    site_admin_url = models.CharField(
        _("админка сайта"),
        max_length=500,
        blank=True,
        help_text=_("URL CMS или админки, без логина и пароля"),
    )
    server_host = models.CharField(
        _("хост сервера"),
        max_length=255,
        blank=True,
        help_text=_("IP или hostname для SSH"),
    )
    server_port = models.PositiveIntegerField(
        _("SSH-порт"),
        default=22,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
    )
    server_username = models.CharField(
        _("пользователь SSH"), max_length=150, blank=True
    )
    server_password = models.CharField(_("пароль SSH"), max_length=255, blank=True)
    server_ssh_key = models.TextField(
        _("SSH-ключ"),
        blank=True,
        help_text=_("Приватный ключ, если вход не по паролю"),
    )
    server_path = models.CharField(
        _("путь на сервере"),
        max_length=500,
        blank=True,
        help_text=_("Каталог проекта, например /var/www/example"),
    )
    extra_credentials = models.TextField(
        _("прочие доступы"),
        blank=True,
        help_text=_(
            "Панель хостинга, CMS, база данных, FTP, API-ключи. "
            "Видит только суперпользователь."
        ),
    )
    internal_notes = models.TextField(
        _("рабочие заметки"),
        blank=True,
        help_text=_(
            "Как деплоить, договорённости с клиентом и прочие постоянные заметки"
        ),
    )
    seo_notes = models.TextField(
        _("SEO-бриф"),
        blank=True,
        help_text=_(
            "Интент, структура, перелинковка, что должно быть в первом экране. "
            "Не попадает в HTML — это задание для страницы."
        ),
    )

    class Meta:
        ordering = ["slug"]
        verbose_name = _("проект")
        verbose_name_plural = _("проекты")

    def __str__(self) -> str:
        return self.slug

    def clean(self) -> None:
        """Normalize public hostnames before validation."""
        super().clean()
        if self.domain:
            self.domain = normalize_host(self.domain)
        if self.staging_domain:
            self.staging_domain = normalize_host(self.staging_domain)


class ProjectNote(BaseModel):
    """A project note that can be forwarded to an employee in Telegram."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name=_("проект"),
    )
    body = models.TextField(_("текст"))
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="received_project_notes",
        verbose_name=_("получатель"),
    )
    telegram_sent = models.BooleanField(_("отправлено в Telegram"), default=False)
    telegram_sent_at = models.DateTimeField(
        _("отправлено"),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("заметка проекта")
        verbose_name_plural = _("заметки проектов")

    def __str__(self) -> str:
        return f"Note<{self.project_id}>"
