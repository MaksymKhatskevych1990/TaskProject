"""Low-level Telegram Bot API client."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from django.conf import settings

from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError

logger = logging.getLogger(__name__)


def _require_enabled() -> str:
    """Return the configured bot token or raise when integration is disabled."""
    if not settings.TELEGRAM_ENABLED:
        raise TelegramDisabledError("Telegram integration is disabled.")
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise TelegramDisabledError("TELEGRAM_BOT_TOKEN is not configured.")
    return token


def call_method(
    method: str,
    payload: dict[str, Any] | None = None,
    *,
    request_timeout: int = 30,
) -> dict[str, Any]:
    """Call a Telegram Bot API method and return the parsed response body."""
    token = _require_enabled()
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload or {}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=request_timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except TimeoutError as exc:
        logger.debug(
            "Telegram API request timed out",
            extra={"method": method, "request_timeout": request_timeout},
        )
        raise TelegramAPIError("Telegram API request timed out.") from exc
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        logger.warning(
            "Telegram API HTTP error",
            extra={"method": method, "status_code": exc.code, "body": error_body},
        )
        raise TelegramAPIError(error_body or str(exc), status_code=exc.code) from exc
    except urllib.error.URLError as exc:
        logger.warning("Telegram API connection error", extra={"method": method})
        raise TelegramAPIError(str(exc)) from exc

    if not body.get("ok"):
        description = body.get("description", "Unknown Telegram API error")
        logger.warning(
            "Telegram API returned error",
            extra={"method": method, "description": description},
        )
        raise TelegramAPIError(description)

    return body


def send_message(
    *,
    chat_id: int,
    text: str,
    parse_mode: str | None = None,
    reply_markup: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send a text message to a Telegram chat."""
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return call_method("sendMessage", payload)


def edit_message_text(
    *,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Edit an existing message and its inline keyboard."""
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
    }
    if reply_markup is not None:
        payload["reply_markup"] = reply_markup
    return call_method("editMessageText", payload)


def answer_callback_query(
    *,
    callback_query_id: str,
    text: str | None = None,
    show_alert: bool = False,
) -> dict[str, Any]:
    """Acknowledge an inline button press."""
    payload: dict[str, Any] = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
        payload["show_alert"] = show_alert
    return call_method("answerCallbackQuery", payload)


def get_updates(*, offset: int | None = None, timeout: int = 30) -> list[dict[str, Any]]:
    """Fetch pending updates using long polling."""
    payload: dict[str, Any] = {"timeout": timeout}
    if offset is not None:
        payload["offset"] = offset
    try:
        body = call_method(
            "getUpdates",
            payload,
            request_timeout=timeout + 15,
        )
    except TelegramAPIError as exc:
        # Long polling often ends with an empty HTTP timeout when no updates arrive.
        if "timed out" in str(exc).lower():
            return []
        raise
    return body.get("result", [])


def set_webhook(*, url: str, secret_token: str | None = None) -> dict[str, Any]:
    """Register the bot webhook URL."""
    payload: dict[str, Any] = {"url": url}
    if secret_token:
        payload["secret_token"] = secret_token
    return call_method("setWebhook", payload)


def delete_webhook() -> dict[str, Any]:
    """Remove the bot webhook."""
    return call_method("deleteWebhook", {"drop_pending_updates": False})


def set_my_commands(*, commands: list[dict[str, str]]) -> dict[str, Any]:
    """Register bot commands shown in the Telegram menu button."""
    return call_method("setMyCommands", {"commands": commands})


def get_file(*, file_id: str) -> dict[str, Any]:
    """Return metadata for a Telegram file."""
    body = call_method("getFile", {"file_id": file_id})
    return body.get("result", {})


def download_file(*, file_path: str, request_timeout: int = 60) -> bytes:
    """Download a file from Telegram servers."""
    token = _require_enabled()
    url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=request_timeout) as response:
            return response.read()
    except TimeoutError as exc:
        raise TelegramAPIError("Telegram file download timed out.") from exc
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise TelegramAPIError(error_body or str(exc), status_code=exc.code) from exc
    except urllib.error.URLError as exc:
        raise TelegramAPIError(str(exc)) from exc


def send_document(
    *,
    chat_id: int,
    document_url: str,
    caption: str | None = None,
) -> dict[str, Any]:
    """Send a document to a Telegram chat by URL."""
    payload: dict[str, Any] = {"chat_id": chat_id, "document": document_url}
    if caption:
        payload["caption"] = caption
    return call_method("sendDocument", payload)
