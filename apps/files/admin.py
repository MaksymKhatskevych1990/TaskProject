"""Django admin integration for file attachments."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.files.models import TaskAttachment


@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    """Manage task attachments from the administration site."""

    list_display = (
        "original_filename",
        "task",
        "file_size",
        "uploaded_by",
        "created_at",
    )
    list_filter = ("content_type", "created_at")
    search_fields = ("original_filename", "task__title", "uploaded_by__email")
    autocomplete_fields = ("task", "uploaded_by")
    readonly_fields = (
        "uuid",
        "file_size",
        "content_type",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    fieldsets = (
        (None, {"fields": ("task", "file", "original_filename", "content_type", "file_size", "uploaded_by")}),
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )
