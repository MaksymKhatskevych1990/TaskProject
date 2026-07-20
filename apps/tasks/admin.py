"""Django admin integration for tasks."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import Task
from apps.telegram import services as telegram_services


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Manage tasks from the administration site."""

    list_display = ("title", "assignee", "status", "due_date", "updated_at")
    list_filter = ("status", "due_date")
    search_fields = ("title", "description", "assignee__email")
    autocomplete_fields = ("assignee",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {"fields": ("title", "description", "assignee", "status", "due_date")}),
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    def save_model(self, request, obj, form, change) -> None:
        """Persist the task and notify the assignee when needed."""
        previous_assignee_id = None
        if change:
            previous_assignee_id = (
                Task.objects.filter(pk=obj.pk)
                .values_list("assignee_id", flat=True)
                .first()
            )

        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

        if not change or previous_assignee_id != obj.assignee_id:
            telegram_services.notify_user_about_task(user=obj.assignee, task=obj)
