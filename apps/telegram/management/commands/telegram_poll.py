"""Poll Telegram updates for local development."""

import time

from django.core.management.base import BaseCommand, CommandError

from apps.telegram import client, services
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError


class Command(BaseCommand):
    """Run long polling against the Telegram Bot API."""

    help = "Poll Telegram updates locally when webhook is unavailable."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--once",
            action="store_true",
            help="Fetch and process a single batch of updates.",
        )

    def handle(self, *args, **options) -> None:
        offset: int | None = None

        try:
            client.delete_webhook()
            self.stdout.write("Webhook отключён — используется polling.")
        except (TelegramDisabledError, TelegramAPIError) as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.SUCCESS("Telegram polling started. Ctrl+C to stop."))

        while True:
            try:
                updates = client.get_updates(offset=offset, timeout=30)
            except TelegramDisabledError as exc:
                raise CommandError(str(exc)) from exc
            except TelegramAPIError as exc:
                self.stderr.write(self.style.WARNING(f"Telegram API error: {exc}"))
                time.sleep(5)
                continue

            for update in updates:
                services.process_webhook_update(update=update)
                offset = update["update_id"] + 1

            if options["once"]:
                break
