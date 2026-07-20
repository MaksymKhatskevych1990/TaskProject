"""Django admin integration for employees."""

from django.contrib import admin

from apps.employees.models import Employee, Position, Team


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Manage job titles."""

    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Manage studio teams."""

    list_display = ("name", "lead", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "lead__email")
    autocomplete_fields = ("lead",)
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Manage employee directory records."""

    list_display = ("user", "team", "position", "hire_date", "updated_at")
    list_filter = ("team", "position", "user__is_active")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "notes",
    )
    autocomplete_fields = ("user", "team", "position")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
