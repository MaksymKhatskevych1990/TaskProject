"""Django admin integration for projects."""

from django import forms
from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.common.seo import SeoFieldsMixin
from apps.common.seo_admin import SEO_ADMIN_MEDIA, SEO_FIELDSET, seo_status_badge
from apps.employees.models import Employee
from apps.projects import selectors, services
from apps.projects.choices import ProjectStatus
from apps.projects.models import Project, ProjectNote

STATUS_COLORS = {
    ProjectStatus.DEVELOPMENT: "#0d6efd",
    ProjectStatus.LAUNCHED: "#198754",
    ProjectStatus.SUPPORT: "#6f42c1",
    ProjectStatus.PAUSED: "#fd7e14",
    ProjectStatus.ARCHIVED: "#6c757d",
}


def format_employee_choice(employee: Employee) -> str:
    """Show a readable employee label in the Telegram recipient list."""
    name = employee.user.full_name
    if employee.position_id:
        return f"{name} · {employee.position.title}"
    return name


class ProjectAdminForm(forms.ModelForm):
    """Project form with a one-shot Telegram note composer."""

    new_note = forms.CharField(
        required=False,
        label=_("Новая заметка"),
        widget=forms.Textarea(attrs={"rows": 4}),
        help_text=_(
            "Сохранится в истории проекта. Если выбрать сотрудника — уйдёт ему в Telegram."
        ),
    )
    note_recipient = forms.ModelChoiceField(
        required=False,
        queryset=Employee.objects.none(),
        label=_("Отправить сотруднику в Telegram"),
        empty_label=_("Не отправлять"),
    )

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        recipient_field = self.fields["note_recipient"]
        recipient_field.queryset = selectors.list_telegram_ready_employees()
        recipient_field.label_from_instance = format_employee_choice

    def clean(self) -> dict:
        """Require note text when a Telegram recipient is selected."""
        cleaned = super().clean()
        recipient = cleaned.get("note_recipient")
        note = (cleaned.get("new_note") or "").strip()
        if recipient is not None and not note:
            self.add_error(
                "new_note",
                _("Напишите заметку, чтобы отправить её в Telegram."),
            )
        return cleaned


class ProjectNoteInline(admin.TabularInline):
    """Show previously saved project notes without allowing inline edits."""

    model = ProjectNote
    extra = 0
    can_delete = False
    autocomplete_fields = ("recipient",)
    readonly_fields = (
        "body",
        "recipient",
        "telegram_sent",
        "created_by",
        "created_at",
    )
    fields = ("body", "recipient", "telegram_sent", "created_by", "created_at")
    verbose_name = _("история заметки")
    verbose_name_plural = _("история заметок")

    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        """Notes are created from the project form so Telegram goes through the service."""
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Manage studio projects from the administration site."""

    form = ProjectAdminForm
    list_display = (
        "slug",
        "name",
        "domain",
        "status_badge",
        "seo_status",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "status")
    search_fields = ("slug", "name", "domain", "staging_domain", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("lead",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    inlines = (ProjectNoteInline,)

    class Media:
        css = SEO_ADMIN_MEDIA["css"]
        js = SEO_ADMIN_MEDIA["js"]

    def get_exclude(self, request: HttpRequest, obj=None):
        """Keep server credentials out of the form for everyone except superusers."""
        exclude = list(super().get_exclude(request, obj) or [])
        if not request.user.is_superuser:
            exclude.extend(Project.SECRET_FIELDS)
        return exclude

    def get_fieldsets(self, request: HttpRequest, obj=None):
        """Hide the server-access tab from staff who are not superusers."""
        fieldsets = [
            (
                None,
                {
                    "fields": (
                        "name",
                        "slug",
                        "is_active",
                        "status",
                        "description",
                        "lead",
                        "started_on",
                        "hosting_provider",
                    )
                },
            ),
            (
                _("Адреса и ссылки"),
                {
                    "fields": (
                        "domain",
                        "staging_domain",
                        "repository_url",
                        "site_admin_url",
                    )
                },
            ),
        ]
        if request.user.is_superuser:
            fieldsets.append(
                (
                    _("Доступ к серверу"),
                    {
                        "description": _(
                            "Эти данные видит только суперпользователь. "
                            "Не копируйте их в заметки и не отправляйте в Telegram."
                        ),
                        "fields": Project.SECRET_FIELDS,
                    },
                )
            )
        fieldsets.extend(
            [
                (
                    SEO_FIELDSET[0],
                    {
                        **SEO_FIELDSET[1],
                        "fields": (*SeoFieldsMixin.SEO_FIELDS, "seo_notes"),
                    },
                ),
                (
                    _("Заметки"),
                    {"fields": ("internal_notes", "new_note", "note_recipient")},
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
            ]
        )
        return fieldsets

    @admin.display(description=_("SEO"))
    def seo_status(self, obj: Project) -> str:
        """Show whether the public snippet fields are filled."""
        return seo_status_badge(obj)

    @admin.display(description=_("Статус"), ordering="status")
    def status_badge(self, obj: Project) -> str:
        """Highlight the current project status in the changelist."""
        color = STATUS_COLORS.get(obj.status, "#6c757d")
        return format_html(
            '<span style="display:inline-block;padding:2px 8px;border-radius:12px;'
            'color:#fff;background:{};font-weight:600;">{}</span>',
            color,
            obj.get_status_display(),
        )

    def save_model(self, request, obj, form, change) -> None:
        """Track audit users and send a composed note through the project service."""
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

        note_text = (form.cleaned_data.get("new_note") or "").strip()
        if not note_text:
            return

        recipient_employee = form.cleaned_data.get("note_recipient")
        recipient = recipient_employee.user if recipient_employee is not None else None
        note = services.create_project_note(
            project=obj,
            body=note_text,
            actor=request.user,
            recipient=recipient,
        )
        if recipient is None:
            messages.success(request, _("Заметка сохранена."))
        elif note.telegram_sent:
            messages.success(
                request,
                _("Заметка отправлена в Telegram: %(name)s")
                % {"name": recipient.full_name},
            )
        else:
            messages.warning(
                request,
                _(
                    "Заметка сохранена, но отправить её в Telegram не удалось. "
                    "Проверьте привязку Telegram у сотрудника."
                ),
            )
