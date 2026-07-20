"""Register or remove the Telegram bot webhook."""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.telegram import client
from apps.telegram.exceptions import TelegramDisabledError


class Command(BaseCommand):
    """Configure Telegram webhook URL for production use."""

    help = "Register the Telegram bot webhook URL."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Remove the webhook instead of registering it.",
        )

    def handle(self, *args, **options) -> None:
        if options["delete"]:
            client.delete_webhook()
            self.stdout.write(self.style.SUCCESS("Telegram webhook removed."))
            return

        if not settings.TELEGRAM_WEBHOOK_URL:
            raise CommandError("TELEGRAM_WEBHOOK_URL is not configured.")

        try:
            client.set_webhook(
                url=settings.TELEGRAM_WEBHOOK_URL,
                secret_token=settings.TELEGRAM_WEBHOOK_SECRET or None,
            )
        except TelegramDisabledError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(f"Telegram webhook registered: {settings.TELEGRAM_WEBHOOK_URL}")
        )
