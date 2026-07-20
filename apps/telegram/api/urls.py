"""Telegram API routes."""

from django.urls import path

from apps.telegram.api.views import TelegramWebhookView

app_name = "telegram"

urlpatterns = [
    path(
        "webhook/<str:secret>/",
        TelegramWebhookView.as_view(),
        name="webhook",
    ),
]
