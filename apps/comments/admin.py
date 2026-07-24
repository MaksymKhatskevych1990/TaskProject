"""Django admin integration for discussions."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.comments.models import Discussion, DiscussionMessage, DiscussionParticipant


class DiscussionParticipantInline(admin.TabularInline):
    """Show discussion members inline."""

    model = DiscussionParticipant
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("uuid", "created_at")


class DiscussionMessageInline(admin.TabularInline):
    """Show recent discussion messages inline."""

    model = DiscussionMessage
    extra = 0
    autocomplete_fields = ("author",)
    readonly_fields = ("uuid", "source", "created_at")
    fields = ("author", "body", "source", "created_at")


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    """Browse discussions from the administration site."""

    list_display = ("task", "created_by", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("task__title", "created_by__email")
    autocomplete_fields = ("task", "created_by")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
    inlines = (DiscussionParticipantInline, DiscussionMessageInline)


@admin.register(DiscussionMessage)
class DiscussionMessageAdmin(admin.ModelAdmin):
    """Browse discussion messages independently when needed."""

    list_display = ("discussion", "author", "source", "created_at")
    list_filter = ("source",)
    search_fields = ("body", "author__email", "discussion__task__title")
    autocomplete_fields = ("discussion", "author")
    readonly_fields = ("uuid", "created_at", "updated_at", "created_by", "updated_by")
