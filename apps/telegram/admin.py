"""Django admin integration for Telegram."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.telegram.models import TelegramAccount


class TelegramAccountInline(admin.StackedInline):
    """Edit Telegram contact data from the user admin page."""

    model = TelegramAccount
    fk_name = "user"
    can_delete = False
    extra = 0
    verbose_name = _("Telegram")
    verbose_name_plural = _("Telegram")
    readonly_fields = ("link_token", "bot_link")
    fields = (
        "username",
        "chat_id",
        "notifications_enabled",
        "link_token",
        "bot_link",
    )


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    """Browse Telegram accounts independently when needed."""

    list_display = (
        "user",
        "username",
        "chat_id",
        "notifications_enabled",
        "updated_at",
    )
    list_filter = ("notifications_enabled",)
    search_fields = ("user__email", "username", "chat_id")
    autocomplete_fields = ("user",)
    readonly_fields = (
        "uuid",
        "link_token",
        "bot_link",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
