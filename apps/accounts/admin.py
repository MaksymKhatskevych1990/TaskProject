"""Django admin integration for accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Profile, User
from apps.telegram.admin import TelegramAccountInline


class ProfileInline(admin.StackedInline):
    """Edit profile data from the user admin page."""

    model = Profile
    fk_name = "user"
    can_delete = False
    extra = 0
    fields = ("phone", "position", "bio", "timezone", "avatar")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Manage users from the administration site."""

    ordering = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "telegram_username_display",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("uuid", "last_login", "date_joined")
    inlines = (ProfileInline, TelegramAccountInline)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Личные данные"), {"fields": ("first_name", "last_name", "role")}),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
        (_("Идентификаторы"), {"fields": ("uuid",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    @admin.display(description=_("Telegram"))
    def telegram_username_display(self, obj: User) -> str:
        """Show linked Telegram username in the user list."""
        account = getattr(obj, "telegram_account", None)
        if account is None or not account.username:
            return "—"
        return f"@{account.username}"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Browse profiles independently when needed."""

    list_display = ("user", "position", "phone", "timezone", "updated_at")
    search_fields = ("user__email", "position", "phone")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
