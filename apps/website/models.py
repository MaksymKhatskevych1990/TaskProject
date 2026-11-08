"""Public website content models."""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.seo import SeoFieldsMixin
from apps.website.choices import BlogPostStatus, PortfolioAccent
from apps.website.text import ensure_unique_slug, is_latin_slug, latin_slugify


def portfolio_cover_upload_to(instance: "PortfolioProject", filename: str) -> str:
    """Build a storage path for portfolio cover images."""
    return f"portfolio/{instance.slug or 'draft'}/cover/{filename}"


def portfolio_gallery_upload_to(
    instance: "PortfolioGalleryImage", filename: str
) -> str:
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


class BlogPost(SeoFieldsMixin, BaseModel):
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
    published_at = models.DateTimeField(
        _("дата публикации"), null=True, blank=True, db_index=True
    )
    read_time_minutes = models.PositiveSmallIntegerField(
        _("время чтения (мин)"), default=5
    )

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


class PortfolioProject(SeoFieldsMixin, BaseModel):
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
        help_text=_(
            "Tailwind-класи для превʼю без обкладинки, напр. from-violet/60 to-cyan/40"
        ),
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
    case_description = models.TextField(
        _("описание кейса"), max_length=2000, blank=True
    )

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
            self.slug = ensure_unique_slug(
                PortfolioProject, base_slug, exclude_pk=self.pk
            )
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


def split_lines(value: str) -> list[str]:
    """Return non-empty trimmed lines from a textarea."""
    return [line.strip() for line in (value or "").splitlines() if line.strip()]


class SiteSeoSettings(SeoFieldsMixin, BaseModel):
    """Singleton landing-page and SEO settings edited as one admin page."""

    brand = models.CharField(
        _("бренд"),
        max_length=120,
        default="Chameleon Digital Studio",
    )
    brand_short = models.CharField(_("короткое имя"), max_length=40, default="Chameleon")
    domain = models.CharField(_("домен"), max_length=120, default="chameleon.digital")
    tagline = models.CharField(
        _("слоган"),
        max_length=160,
        default="IT-студія | Сайти, магазини, Telegram-боти",
    )
    site_description = models.TextField(
        _("описание студии"),
        default=(
            "Запустимо ваш бізнес онлайн. Сайти, інтернет-магазини, "
            "Telegram-боти та автоматизація під ключ за фіксованою ціною."
        ),
    )
    email = models.EmailField(_("email"), default="hello@chameleon.digital")
    phone = models.CharField(_("телефон"), max_length=40, default="+380937090317")
    telegram_username = models.CharField(
        _("Telegram username"),
        max_length=64,
        default="devcraft_studio",
        help_text=_("Без @"),
    )
    telegram_url = models.URLField(
        _("ссылка Telegram"),
        default="https://t.me/devcraft_studio",
    )
    founding_year = models.PositiveIntegerField(_("год основания"), default=2020)
    currency = models.CharField(_("валюта"), max_length=8, default="₴")
    locale = models.CharField(_("локаль"), max_length=16, default="uk-UA")
    footer_about = models.TextField(
        _("текст в подвале"),
        default=(
            "Digital-студія з Дніпра. Сайти, магазини й боти під ключ для клієнтів "
            "по Україні та ЄС — повністю онлайн."
        ),
    )
    footer_rights = models.CharField(
        _("копирайт"),
        max_length=160,
        default="Усі права захищені.",
    )
    footer_blog_label = models.CharField(_("ссылка на блог"), max_length=40, default="Блог")
    footer_telegram_label = models.CharField(
        _("ссылка Telegram в подвале"),
        max_length=40,
        default="Telegram",
    )
    footer_write_telegram = models.CharField(
        _("кнопка написать в Telegram"),
        max_length=80,
        default="Написати в Telegram",
    )
    footer_offices_label = models.CharField(
        _("подвал · офисы"),
        max_length=40,
        default="Локація",
    )
    footer_faq_label = models.CharField(
        _("подвал · FAQ"),
        max_length=40,
        default="FAQ",
    )
    hero_status = models.CharField(_("статус Hero"), max_length=80, default="2 вільні слоти")
    hero_status_meta = models.CharField(
        _("пояснение статуса"),
        max_length=160,
        default="вересень 2026 · старт можна узгодити цього тижня",
    )
    hero_title = models.CharField(
        _("заголовок Hero"),
        max_length=150,
        default="Розробка сайтів під ключ",
    )
    hero_hint = models.CharField(
        _("подзаголовок Hero"),
        max_length=250,
        default=(
            "Оберіть задачу — одразу побачите термін, склад і ціну. "
            "Договір до старту, відповідь у Telegram за 30 хвилин."
        ),
    )
    hero_primary_cta = models.CharField(
        _("кнопка Hero"),
        max_length=80,
        default="Отримати розрахунок",
    )
    hero_secondary_cta = models.CharField(
        _("вторая кнопка Hero"),
        max_length=80,
        default="Живі сайти",
    )
    hero_conditions = models.TextField(
        _("условия под Hero"),
        default="Ціна фіксується в договорі\n2 раунди правок\n30 днів підтримки після запуску",
        help_text=_("Каждая строка — отдельный пункт."),
    )
    hero_chameleon_label = models.CharField(
        _("Hero · подпись хамелеона"),
        max_length=200,
        default="Chameleon Digital Studio — наведи курсор, щоб хамелеон повернув голову",
    )
    services_eyebrow = models.CharField(_("услуги · метка"), max_length=40, default="Послуги")
    services_title = models.CharField(_("услуги · заголовок"), max_length=120, default="Що ми робимо")
    services_subtitle = models.TextField(
        _("услуги · описание"),
        default=(
            "Дизайн, розробка та просування — три напрямки, які закривають "
            "повний цикл вашого digital-проєкту."
        ),
    )
    services_also = models.CharField(_("услуги · также"), max_length=40, default="Також")
    cases_eyebrow = models.CharField(_("кейсы · метка"), max_length=40, default="Кейси")
    cases_title = models.CharField(
        _("кейсы · заголовок"),
        max_length=120,
        default="Результати клієнтів",
    )
    cases_subtitle = models.TextField(
        _("кейсы · описание"),
        default="Одна схема для кожного кейсу: що було, що стало і який ефект.",
    )
    cases_before_label = models.CharField(_("кейсы · было"), max_length=40, default="Було")
    cases_after_label = models.CharField(_("кейсы · стало"), max_length=40, default="Стало")
    cases_result_label = models.CharField(_("кейсы · результат"), max_length=40, default="Результат")
    portfolio_eyebrow = models.CharField(_("портфолио · метка"), max_length=40, default="Портфоліо")
    portfolio_title = models.CharField(
        _("портфолио · заголовок"),
        max_length=120,
        default="Наші роботи",
    )
    portfolio_subtitle = models.TextField(
        _("портфолио · описание"),
        default="Реальні проєкти — від дизайну та лендингів до інтернет-магазинів і SEO.",
    )
    portfolio_cta = models.CharField(
        _("портфолио · кнопка"),
        max_length=80,
        default="Обговорити схожий проєкт",
    )
    process_eyebrow = models.CharField(_("процесс · метка"), max_length=40, default="Процес")
    process_title = models.CharField(
        _("процесс · заголовок"),
        max_length=120,
        default="Як ми працюємо",
    )
    process_subtitle = models.TextField(
        _("процесс · описание"),
        default="Від першого дзвінка до запуску — прозорий процес без сюрпризів.",
    )
    pricing_eyebrow = models.CharField(_("цены · метка"), max_length=40, default="Ціни")
    pricing_title = models.CharField(
        _("цены · заголовок"),
        max_length=120,
        default="Прозорі тарифи",
    )
    pricing_subtitle = models.TextField(
        _("цены · описание"),
        default="Усі ціни вказані в гривнях. Фіксуємо вартість у договорі.",
    )
    pricing_from_label = models.CharField(_("цены · от"), max_length=20, default="від")
    pricing_cta = models.CharField(
        _("цены · кнопка"),
        max_length=80,
        default="Обрати тариф",
    )
    guarantees_eyebrow = models.CharField(_("гарантии · метка"), max_length=40, default="Гарантії")
    guarantees_title = models.CharField(
        _("гарантии · заголовок"),
        max_length=120,
        default="Працюємо без ризиків",
    )
    faq_eyebrow = models.CharField(_("FAQ · метка"), max_length=40, default="FAQ")
    faq_title = models.CharField(
        _("FAQ · заголовок"),
        max_length=120,
        default="Часті запитання",
    )
    contact_title = models.CharField(
        _("форма · заголовок"),
        max_length=160,
        default="Готові запустити проєкт?",
    )
    contact_subtitle = models.TextField(
        _("форма · описание"),
        default="Залиште заявку — відповімо в Telegram протягом 30 хвилин.",
    )
    contact_submit = models.CharField(
        _("форма · кнопка"),
        max_length=80,
        default="Отримати розрахунок",
    )
    contact_submitting = models.CharField(
        _("форма · отправка"),
        max_length=80,
        default="Надсилаємо...",
    )
    contact_success_title = models.CharField(
        _("форма · успех"),
        max_length=160,
        default="Заявку надіслано!",
    )
    contact_success_subtitle = models.TextField(
        _("форма · успех текст"),
        default="Перенаправляємо вас у Telegram для продовження діалогу…",
    )
    contact_error = models.CharField(
        _("форма · ошибка"),
        max_length=200,
        default="Не вдалося надіслати заявку. Спробуйте написати нам у Telegram.",
    )
    contact_name_label = models.CharField(_("поле имя"), max_length=80, default="Ім'я")
    contact_name_placeholder = models.CharField(
        _("плейсхолдер имени"),
        max_length=80,
        default="Як до вас звертатись?",
    )
    contact_phone_label = models.CharField(
        _("поле контакт"),
        max_length=80,
        default="Телефон або Telegram",
    )
    contact_phone_placeholder = models.CharField(
        _("плейсхолдер контакта"),
        max_length=80,
        default="@username або +380...",
    )
    contact_project_label = models.CharField(
        _("поле проект"),
        max_length=80,
        default="Про проєкт",
    )
    contact_project_placeholder = models.CharField(
        _("плейсхолдер проекта"),
        max_length=80,
        default="Коротко опишіть задачу...",
    )
    contact_plan_label = models.CharField(
        _("поле тариф"),
        max_length=80,
        default="Тариф",
    )
    blog_page_eyebrow = models.CharField(_("блог · метка"), max_length=40, default="Блог")
    blog_page_title = models.CharField(
        _("блог · заголовок"),
        max_length=120,
        default="Корисні матеріали",
    )
    blog_page_subtitle = models.TextField(
        _("блог · описание"),
        default="Поради з дизайну, розробки та SEO — від нашої команди.",
    )
    blog_read_more = models.CharField(_("блог · читать"), max_length=40, default="Читати далі")
    blog_back_label = models.CharField(
        _("блог · назад"),
        max_length=40,
        default="← До блогу",
    )
    blog_read_time_label = models.CharField(
        _("блог · время чтения"),
        max_length=40,
        default="хв читання",
    )
    blog_empty = models.CharField(
        _("блог · пусто"),
        max_length=120,
        default="Статті з'являться незабаром.",
    )
    blog_cta_title = models.CharField(
        _("блог · CTA заголовок"),
        max_length=160,
        default="Потрібна допомога з проєктом?",
    )
    blog_cta_subtitle = models.TextField(
        _("блог · CTA текст"),
        default="Розкажіть про задачу — відповімо в Telegram протягом 30 хвилин.",
    )
    blog_cta_button = models.CharField(
        _("блог · CTA кнопка"),
        max_length=80,
        default="Розпочати проєкт",
    )
    blog_title = models.CharField(
        _("Title страницы блога"),
        max_length=70,
        blank=True,
        help_text=_("Заголовок вкладки и сниппета для /blog. 50–60 символов."),
    )
    blog_description = models.CharField(
        _("Description страницы блога"),
        max_length=180,
        blank=True,
        help_text=_("Сниппет раздела блога. 140–160 символов."),
    )
    blog_h1 = models.CharField(
        _("H1 страницы блога"),
        max_length=150,
        blank=True,
        help_text=_("Заголовок на странице /blog. Если пусто — оставим текущий."),
    )
    google_site_verification = models.CharField(
        _("Google Search Console"),
        max_length=200,
        blank=True,
        help_text=_("Код верификации из Search Console, только значение content."),
    )

    class Meta:
        verbose_name = _("настройки сайта")
        verbose_name_plural = _("настройки сайта")

    def __str__(self) -> str:
        return "Настройки сайта"

    @property
    def telegram_handle(self) -> str:
        """Return the Telegram username without a leading @."""
        return (self.telegram_username or "").lstrip("@")

    def save(self, *args, **kwargs) -> None:
        """Keep a single settings row."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """Prevent deleting the singleton settings row."""
        return None


class SiteOwnedModel(BaseModel):
    """A repeatable block that belongs to the singleton site settings."""

    site = models.ForeignKey(
        SiteSeoSettings,
        on_delete=models.CASCADE,
        related_name="%(class)s_items",
        verbose_name=_("настройки сайта"),
    )
    ordering = models.PositiveIntegerField(_("порядок"), default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["ordering", "id"]


class SiteNavLink(SiteOwnedModel):
    """Header navigation item."""

    href = models.CharField(_("ссылка"), max_length=200)
    label = models.CharField(_("текст"), max_length=80)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("пункт меню")
        verbose_name_plural = _("меню")

    def __str__(self) -> str:
        return self.label


class SiteHeroOffer(SiteOwnedModel):
    """Selectable offer in the hero block."""

    slug = models.SlugField(_("ключ"), max_length=40)
    label = models.CharField(_("название"), max_length=80)
    duration = models.CharField(_("срок"), max_length=80)
    price = models.PositiveIntegerField(_("цена"))
    plan = models.CharField(_("тариф"), max_length=40, blank=True)
    includes = models.TextField(_("что входит"))

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("предложение Hero")
        verbose_name_plural = _("Hero · предложения")

    def __str__(self) -> str:
        return self.label


class SiteService(SiteOwnedModel):
    """Service card on the landing page."""

    title = models.CharField(_("название"), max_length=120)
    description = models.TextField(_("описание"))
    features = models.TextField(
        _("пункты"),
        blank=True,
        help_text=_("Каждая строка — отдельный пункт."),
    )
    featured = models.BooleanField(_("основная услуга"), default=True)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("услуга")
        verbose_name_plural = _("услуги")

    def __str__(self) -> str:
        return self.title


class SiteStat(SiteOwnedModel):
    """Numeric social-proof stat."""

    value = models.FloatField(_("значение"))
    suffix = models.CharField(_("суффикс"), max_length=20, blank=True)
    label = models.CharField(_("подпись"), max_length=80)
    decimals = models.PositiveSmallIntegerField(_("знаки после запятой"), default=0)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("цифра")
        verbose_name_plural = _("цифры")

    def __str__(self) -> str:
        return self.label


class SiteTestimonial(SiteOwnedModel):
    """Client quote."""

    name = models.CharField(_("имя"), max_length=80)
    role = models.CharField(_("роль"), max_length=120, blank=True)
    text = models.TextField(_("цитата"))
    rating = models.PositiveSmallIntegerField(_("оценка"), default=5)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("отзыв")
        verbose_name_plural = _("отзывы")

    def __str__(self) -> str:
        return self.name


class SiteCaseStudy(SiteOwnedModel):
    """Before/after case on the landing page."""

    category = models.CharField(_("категория"), max_length=80)
    title = models.CharField(_("название"), max_length=160)
    description = models.TextField(_("описание"), blank=True)
    before_value = models.CharField(_("было"), max_length=120)
    after_value = models.CharField(_("стало"), max_length=120)
    metric = models.CharField(_("метрика"), max_length=40)
    metric_label = models.CharField(_("подпись метрики"), max_length=80, blank=True)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("кейс")
        verbose_name_plural = _("кейсы")

    def __str__(self) -> str:
        return self.title


class SiteProcessStep(SiteOwnedModel):
    """Process step."""

    title = models.CharField(_("название"), max_length=120)
    description = models.TextField(_("описание"))

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("шаг процесса")
        verbose_name_plural = _("процесс")

    def __str__(self) -> str:
        return self.title


class SitePricingPlan(SiteOwnedModel):
    """Pricing card."""

    slug = models.SlugField(_("ключ"), max_length=40)
    name = models.CharField(_("название"), max_length=80)
    price = models.PositiveIntegerField(_("цена"))
    description = models.TextField(_("описание"), blank=True)
    features = models.TextField(
        _("пункты"),
        help_text=_("Каждая строка — отдельный пункт."),
    )
    highlighted = models.BooleanField(_("выделить"), default=False)
    badge = models.CharField(_("бейдж"), max_length=40, blank=True)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("тариф")
        verbose_name_plural = _("тарифы")

    def __str__(self) -> str:
        return self.name


class SiteGuarantee(SiteOwnedModel):
    """Guarantee card."""

    class ImageKey(models.TextChoices):
        PRICE = "price", _("цена")
        TERM = "term", _("срок")
        EDITS = "edits", _("правки")
        SUPPORT = "support", _("поддержка")

    title = models.CharField(_("название"), max_length=120)
    description = models.TextField(_("описание"))
    image_key = models.CharField(
        _("иконка"),
        max_length=20,
        choices=ImageKey.choices,
        default=ImageKey.PRICE,
    )

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("гарантия")
        verbose_name_plural = _("гарантии")

    def __str__(self) -> str:
        return self.title


class SiteFaqItem(SiteOwnedModel):
    """FAQ row."""

    question = models.CharField(_("вопрос"), max_length=200)
    answer = models.TextField(_("ответ"))

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("вопрос FAQ")
        verbose_name_plural = _("FAQ")

    def __str__(self) -> str:
        return self.question


class SiteOffice(SiteOwnedModel):
    """Office shown in the footer and local SEO."""

    slug = models.SlugField(_("ключ"), max_length=40)
    name = models.CharField(_("город"), max_length=80)
    label = models.CharField(_("подпись"), max_length=120, blank=True)
    street_address = models.CharField(_("улица"), max_length=160, blank=True)
    address_locality = models.CharField(_("город"), max_length=80)
    address_region = models.CharField(_("область"), max_length=80, blank=True)
    postal_code = models.CharField(_("индекс"), max_length=20, blank=True)
    address_country = models.CharField(_("страна"), max_length=8, default="UA")
    latitude = models.FloatField(_("широта"), default=0)
    longitude = models.FloatField(_("долгота"), default=0)
    telephone = models.CharField(_("телефон"), max_length=40, blank=True)
    is_headquarters = models.BooleanField(_("головной офис"), default=False)

    class Meta(SiteOwnedModel.Meta):
        verbose_name = _("офис")
        verbose_name_plural = _("офисы")

    def __str__(self) -> str:
        return self.name
