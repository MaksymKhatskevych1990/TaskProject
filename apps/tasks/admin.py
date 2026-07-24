"""Django admin integration for tasks."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.tasks.choices import TaskStatus
from apps.tasks.models import Task
from apps.telegram import services as telegram_services

STATUS_COLORS = {
    TaskStatus.TODO: "#6c757d",
    TaskStatus.IN_PROGRESS: "#0d6efd",
    TaskStatus.DONE: "#198754",
    TaskStatus.CANCELLED: "#dc3545",
}

PROGRESS_LABELS = {
    TaskStatus.TODO: "1/3 · К выполнению",
    TaskStatus.IN_PROGRESS: "2/3 · В работе",
    TaskStatus.DONE: "3/3 · Выполнена",
    TaskStatus.CANCELLED: "— · Отменена",
}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Manage tasks from the administration site."""

    list_display = (
        "title",
        "project",
        "assignee",
        "progress_display",
        "status_badge",
        "due_date",
        "updated_at",
    )
    list_filter = ("status", "project", "due_date", "assignee")
    search_fields = ("title", "description", "assignee__email", "project__slug")
    autocomplete_fields = ("assignee", "project")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    fieldsets = (
        (None, {"fields": ("title", "description", "project", "assignee", "status", "due_date")}),
        (
            _("Служебные поля"),
            {"fields": ("uuid", "created_at", "updated_at", "created_by", "updated_by")},
        ),
    )

    @admin.display(description=_("Прогресс"), ordering="status")
    def progress_display(self, obj: Task) -> str:
        """Show a simple progress label synced with task status."""
        return PROGRESS_LABELS.get(obj.status, obj.get_status_display())

    @admin.display(description=_("Статус"), ordering="status")
    def status_badge(self, obj: Task) -> str:
        """Highlight the current task status in the changelist."""
        color = STATUS_COLORS.get(obj.status, "#6c757d")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:12px;'
            'color:#fff;background:{};font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
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
