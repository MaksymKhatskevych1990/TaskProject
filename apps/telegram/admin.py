"""Django admin integration for Telegram."""

from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from apps.telegram.models import TelegramAccount
from apps.telegram.services import ensure_telegram_account


class TelegramAccountInlineFormSet(BaseInlineFormSet):
    """Update the placeholder Telegram account instead of inserting a duplicate."""

    def save_new(self, form, commit=True):
        """Bind inline data to the account created by the user post-save signal."""
        user = form.instance.user if form.instance.user_id else self.instance
        cleaned = form.cleaned_data
        account = ensure_telegram_account(user=user)
        account.username = cleaned.get("username", "")
        account.chat_id = cleaned.get("chat_id")
        account.notifications_enabled = cleaned.get("notifications_enabled", True)
        account.save()
        form.instance = account
        return account


class TelegramAccountInline(admin.StackedInline):
    """Edit Telegram contact data from the user admin page."""

    model = TelegramAccount
    formset = TelegramAccountInlineFormSet
    fk_name = "user"
    can_delete = False
    extra = 0
    max_num = 1
    min_num = 1
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
