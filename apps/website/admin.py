"""Django admin integration for the public website."""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.common.seo_admin import SEO_ADMIN_MEDIA, SEO_FIELDSET, seo_status_badge
from apps.website.choices import BlogPostStatus
from apps.website.models import (
    BlogCategory,
    BlogPost,
    ContactLead,
    PortfolioGalleryImage,
    PortfolioProject,
    SiteCaseStudy,
    SiteFaqItem,
    SiteGuarantee,
    SiteHeroOffer,
    SiteNavLink,
    SiteOffice,
    SitePricingPlan,
    SiteProcessStep,
    SiteSeoSettings,
    SiteService,
    SiteStat,
    SiteTestimonial,
)

STATUS_COLORS = {
    BlogPostStatus.DRAFT: "#6c757d",
    BlogPostStatus.PUBLISHED: "#198754",
}


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    """Manage blog categories for the marketing site."""

    list_display = ("name", "slug", "ordering", "updated_at")
    list_editable = ("ordering",)
    search_fields = ("name", "slug")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {"fields": ("name", "slug", "ordering")}),
        (
            _("Служебные поля"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )

    class Media:
        js = ("website/admin/latin_slugify.js",)

    def save_model(self, request, obj, form, change) -> None:
        """Track audit users on save."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Manage blog posts for the marketing site."""

    list_display = (
        "title",
        "category",
        "status_badge",
        "seo_status",
        "published_at",
        "read_time_minutes",
        "updated_at",
    )
    list_filter = ("status", "category", "published_at")
    search_fields = ("title", "slug", "excerpt", "content")
    autocomplete_fields = ("category",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    date_hierarchy = "published_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "excerpt",
                    "content",
                    "status",
                    "published_at",
                    "read_time_minutes",
                )
            },
        ),
        SEO_FIELDSET,
        (
            _("Служебные поля"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )

    class Media:
        css = SEO_ADMIN_MEDIA["css"]
        js = ("website/admin/latin_slugify.js",) + SEO_ADMIN_MEDIA["js"]

    @admin.display(description=_("SEO"))
    def seo_status(self, obj: BlogPost) -> str:
        """Show whether the public snippet fields are filled."""
        return seo_status_badge(obj)

    @admin.display(description=_("Статус"), ordering="status")
    def status_badge(self, obj: BlogPost) -> str:
        """Highlight the publication status in the changelist."""
        color = STATUS_COLORS.get(obj.status, "#6c757d")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:12px;'
            'color:#fff;background:{};font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
        )

    def save_model(self, request, obj, form, change) -> None:
        """Track audit users on save."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    """Review contact form submissions from the landing page."""

    list_display = ("name", "phone", "plan", "is_processed", "created_at")
    list_filter = ("is_processed", "plan", "created_at")
    search_fields = ("name", "phone", "project", "plan")
    readonly_fields = (
        "uuid",
        "name",
        "phone",
        "project",
        "plan",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    list_editable = ("is_processed",)
    fieldsets = (
        (None, {"fields": ("name", "phone", "plan", "project", "is_processed")}),
        (
            _("Служебные поля"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )

    def has_add_permission(self, request) -> bool:
        """Contact leads are created only from the public form."""
        return False


class PortfolioGalleryImageInline(admin.TabularInline):
    """Manage gallery images for a portfolio project."""

    model = PortfolioGalleryImage
    extra = 1
    fields = ("image", "caption", "ordering")
    ordering = ("ordering",)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    """Manage portfolio projects for the marketing site."""

    list_display = (
        "title",
        "category",
        "status_badge",
        "seo_status",
        "featured",
        "sort_order",
        "updated_at",
    )
    list_filter = ("status", "featured", "accent", "category")
    list_editable = ("featured", "sort_order")
    search_fields = ("title", "slug", "category", "description", "tags")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    inlines = (PortfolioGalleryImageInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "description",
                    "tags",
                    "accent",
                    "gradient",
                    "cover_image",
                    "client_url",
                    "featured",
                    "sort_order",
                    "status",
                )
            },
        ),
        (
            _("Кейс"),
            {
                "fields": (
                    "metric",
                    "before_label",
                    "after_label",
                    "case_description",
                )
            },
        ),
        SEO_FIELDSET,
        (
            _("Служебные поля"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )

    class Media:
        css = SEO_ADMIN_MEDIA["css"]
        js = ("website/admin/latin_slugify.js",) + SEO_ADMIN_MEDIA["js"]

    @admin.display(description=_("SEO"))
    def seo_status(self, obj: PortfolioProject) -> str:
        """Show whether the public snippet fields are filled."""
        return seo_status_badge(obj)

    @admin.display(description=_("Статус"), ordering="status")
    def status_badge(self, obj: PortfolioProject) -> str:
        """Highlight the publication status in the changelist."""
        color = STATUS_COLORS.get(obj.status, "#6c757d")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:12px;'
            'color:#fff;background:{};font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
        )

    def save_model(self, request, obj, form, change) -> None:
        """Track audit users on save."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class SiteBlockInline(admin.TabularInline):
    """Shared inline options for landing-page blocks."""

    extra = 0
    ordering = ("ordering",)


class SiteNavLinkInline(SiteBlockInline):
    """Edit header navigation links."""

    model = SiteNavLink
    fields = ("href", "label", "ordering")


class SiteHeroOfferInline(admin.StackedInline):
    """Edit selectable hero offers."""

    model = SiteHeroOffer
    extra = 0
    ordering = ("ordering",)
    fields = ("slug", "label", "duration", "price", "plan", "includes", "ordering")


class SiteServiceInline(admin.StackedInline):
    """Edit service cards."""

    model = SiteService
    extra = 0
    ordering = ("ordering",)
    fields = ("title", "description", "features", "featured", "ordering")


class SiteStatInline(SiteBlockInline):
    """Edit social-proof numbers."""

    model = SiteStat
    fields = ("value", "suffix", "label", "decimals", "ordering")


class SiteTestimonialInline(admin.StackedInline):
    """Edit client quotes."""

    model = SiteTestimonial
    extra = 0
    ordering = ("ordering",)
    fields = ("name", "role", "text", "rating", "ordering")


class SiteCaseStudyInline(admin.StackedInline):
    """Edit landing-page case studies."""

    model = SiteCaseStudy
    extra = 0
    ordering = ("ordering",)
    fields = (
        "category",
        "title",
        "description",
        "before_value",
        "after_value",
        "metric",
        "metric_label",
        "ordering",
    )


class SiteProcessStepInline(admin.StackedInline):
    """Edit process steps."""

    model = SiteProcessStep
    extra = 0
    ordering = ("ordering",)
    fields = ("title", "description", "ordering")


class SitePricingPlanInline(admin.StackedInline):
    """Edit pricing cards."""

    model = SitePricingPlan
    extra = 0
    ordering = ("ordering",)
    fields = (
        "slug",
        "name",
        "price",
        "description",
        "features",
        "highlighted",
        "badge",
        "ordering",
    )


class SiteGuaranteeInline(SiteBlockInline):
    """Edit guarantee cards."""

    model = SiteGuarantee
    fields = ("title", "description", "image_key", "ordering")


class SiteFaqItemInline(admin.StackedInline):
    """Edit FAQ rows."""

    model = SiteFaqItem
    extra = 0
    ordering = ("ordering",)
    fields = ("question", "answer", "ordering")


class SiteOfficeInline(admin.StackedInline):
    """Edit offices shown in the footer and local SEO."""

    model = SiteOffice
    extra = 0
    ordering = ("ordering",)
    fields = (
        "slug",
        "name",
        "label",
        "street_address",
        "address_locality",
        "address_region",
        "postal_code",
        "address_country",
        "latitude",
        "longitude",
        "telephone",
        "is_headquarters",
        "ordering",
    )


@admin.register(SiteSeoSettings)
class SiteSeoSettingsAdmin(admin.ModelAdmin):
    """Edit every public landing-page text block from one settings page."""

    list_display = ("__str__", "brand", "email", "seo_status", "updated_at")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    inlines = (
        SiteNavLinkInline,
        SiteHeroOfferInline,
        SiteServiceInline,
        SiteStatInline,
        SiteTestimonialInline,
        SiteCaseStudyInline,
        SiteProcessStepInline,
        SitePricingPlanInline,
        SiteGuaranteeInline,
        SiteFaqItemInline,
        SiteOfficeInline,
    )
    fieldsets = (
        (
            _("Контакты"),
            {
                "description": _(
                    "Бренд, контакты и подвал. Эти значения идут на весь публичный сайт."
                ),
                "fields": (
                    "brand",
                    "brand_short",
                    "domain",
                    "tagline",
                    "site_description",
                    "email",
                    "phone",
                    "telegram_username",
                    "telegram_url",
                    "founding_year",
                    "currency",
                    "locale",
                    "footer_about",
                    "footer_rights",
                    "footer_blog_label",
                    "footer_telegram_label",
                    "footer_write_telegram",
                    "footer_offices_label",
                    "footer_faq_label",
                ),
            },
        ),
        (
            _("Hero"),
            {
                "fields": (
                    "hero_status",
                    "hero_status_meta",
                    "hero_title",
                    "hero_hint",
                    "hero_primary_cta",
                    "hero_secondary_cta",
                    "hero_conditions",
                    "hero_chameleon_label",
                ),
            },
        ),
        (
            _("Секции"),
            {
                "description": _(
                    "Заголовки блоков на главной. Карточки внутри блоков — "
                    "на соседних вкладках."
                ),
                "fields": (
                    "services_eyebrow",
                    "services_title",
                    "services_subtitle",
                    "services_also",
                    "cases_eyebrow",
                    "cases_title",
                    "cases_subtitle",
                    "cases_before_label",
                    "cases_after_label",
                    "cases_result_label",
                    "portfolio_eyebrow",
                    "portfolio_title",
                    "portfolio_subtitle",
                    "portfolio_cta",
                    "process_eyebrow",
                    "process_title",
                    "process_subtitle",
                    "pricing_eyebrow",
                    "pricing_title",
                    "pricing_subtitle",
                    "pricing_from_label",
                    "pricing_cta",
                    "guarantees_eyebrow",
                    "guarantees_title",
                    "faq_eyebrow",
                    "faq_title",
                ),
            },
        ),
        (
            _("Форма"),
            {
                "fields": (
                    "contact_title",
                    "contact_subtitle",
                    "contact_submit",
                    "contact_submitting",
                    "contact_success_title",
                    "contact_success_subtitle",
                    "contact_error",
                    "contact_name_label",
                    "contact_name_placeholder",
                    "contact_phone_label",
                    "contact_phone_placeholder",
                    "contact_project_label",
                    "contact_project_placeholder",
                    "contact_plan_label",
                ),
            },
        ),
        (
            _("Блог"),
            {
                "fields": (
                    "blog_page_eyebrow",
                    "blog_page_title",
                    "blog_page_subtitle",
                    "blog_read_more",
                    "blog_back_label",
                    "blog_read_time_label",
                    "blog_empty",
                    "blog_cta_title",
                    "blog_cta_subtitle",
                    "blog_cta_button",
                    "blog_title",
                    "blog_description",
                    "blog_h1",
                ),
            },
        ),
        (
            _("SEO"),
            {
                "description": _(
                    "Title и description главной страницы. Это самый важный сниппет сайта."
                ),
                "fields": (
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
                    "google_site_verification",
                ),
            },
        ),
        (
            _("Служебные поля"),
            {
                "fields": (
                    "uuid",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                )
            },
        ),
    )
    jazzmin_section_order = (
        "Контакты",
        "Hero",
        "Секции",
        "меню",
        "Hero · предложения",
        "услуги",
        "цифры",
        "отзывы",
        "кейсы",
        "процесс",
        "тарифы",
        "гарантии",
        "FAQ",
        "офисы",
        "Форма",
        "Блог",
        "SEO",
        "Служебные поля",
    )

    class Media:
        css = SEO_ADMIN_MEDIA["css"]
        js = SEO_ADMIN_MEDIA["js"]

    @admin.display(description=_("SEO"))
    def seo_status(self, obj: SiteSeoSettings) -> str:
        """Show whether the homepage snippet is filled."""
        return seo_status_badge(obj)

    def has_add_permission(self, request) -> bool:
        """Only one settings row is allowed."""
        return not SiteSeoSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        """Keep the singleton row."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Open the singleton settings page instead of a list."""
        obj, _created = SiteSeoSettings.objects.get_or_create(pk=1)
        return redirect(reverse("admin:website_siteseosettings_change", args=[obj.pk]))

    def save_model(self, request, obj, form, change) -> None:
        """Track audit users on save."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change) -> None:
        """Assign audit users on landing-page blocks."""
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in instances:
            if obj.pk is None:
                obj.created_by = request.user
            obj.updated_by = request.user
            obj.save()
        formset.save_m2m()
