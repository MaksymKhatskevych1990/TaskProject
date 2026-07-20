"""Consistent response builders for project APIs."""

from typing import Any

from rest_framework.response import Response


def success_response(
    data: Any = None,
    *,
    message: str | None = None,
    status_code: int = 200,
) -> Response:
    """Build a successful API response."""
    payload: dict[str, Any] = {"success": True, "data": data}
    if message is not None:
        payload["message"] = message
    return Response(payload, status=status_code)


def error_response(
    *,
    code: Any,
    message: str,
    details: Any = None,
    status_code: int = 400,
) -> Response:
    """Build an error API response."""
    return Response(
        {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
        },
        status=status_code,
    )
