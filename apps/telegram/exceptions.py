"""Telegram integration errors."""


class TelegramError(Exception):
    """Base Telegram integration error."""


class TelegramDisabledError(TelegramError):
    """Raised when Telegram integration is turned off."""


class TelegramAPIError(TelegramError):
    """Raised when the Telegram Bot API returns an error."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
