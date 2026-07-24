"""Django admin integration for projects."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Manage studio projects from the administration site."""

    list_display = ("slug", "name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("slug", "name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {"fields": ("name", "slug", "is_active")}),
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    def save_model(self, request, obj, form, change) -> None:
        """Track who created or updated the project."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
