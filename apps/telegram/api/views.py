"""Telegram API views."""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.telegram import services


@method_decorator(csrf_exempt, name="dispatch")
class TelegramWebhookView(APIView):
    """Receive Telegram Bot API webhook updates."""

    authentication_classes: list = []
    permission_classes: list = []
    parser_classes = [JSONParser]

    def post(self, request: Request, secret: str) -> Response:
        """Validate the webhook secret and process the update payload."""
        from django.conf import settings

        expected_secret = settings.TELEGRAM_WEBHOOK_SECRET
        if not expected_secret or secret != expected_secret:
            return Response(status=status.HTTP_403_FORBIDDEN)

        update = request.data
        if isinstance(update, dict):
            services.process_webhook_update(update=update)
        return Response({"ok": True})
