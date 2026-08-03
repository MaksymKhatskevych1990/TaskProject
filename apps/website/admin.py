"""Django admin integration for the public website."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.website.choices import BlogPostStatus
from apps.website.models import BlogCategory, BlogPost, ContactLead, PortfolioGalleryImage, PortfolioProject

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
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
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
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    class Media:
        js = ("website/admin/latin_slugify.js",)

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
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
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
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    class Media:
        js = ("website/admin/latin_slugify.js",)

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
