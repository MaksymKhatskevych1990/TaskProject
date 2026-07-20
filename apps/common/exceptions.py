"""Central API exceptions and exception handling."""

import logging
from typing import Any

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.common.responses import error_response

logger = logging.getLogger(__name__)


class ConflictError(APIException):
    """Report a request that conflicts with current resource state."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "The request conflicts with the current resource state."
    default_code = "conflict"


class ServiceUnavailableError(APIException):
    """Report a temporarily unavailable dependency or operation."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "The requested operation is temporarily unavailable."
    default_code = "service_unavailable"


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Convert DRF and unexpected exceptions to the project error envelope."""
    response = drf_exception_handler(exc, context)
    if response is None:
        logger.exception(
            "Unhandled API exception",
            extra={"view": context.get("view").__class__.__name__},
        )
        return error_response(
            code="internal_error",
            message="An unexpected error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, ValidationError):
        code: Any = "validation_error"
        message = "The submitted data is invalid."
    elif isinstance(exc, APIException):
        code = exc.default_code
        detail = (
            response.data.get("detail")
            if isinstance(response.data, dict)
            else None
        )
        message = str(detail or exc.default_detail)
    else:
        code = "request_error"
        message = "The request could not be completed."

    if response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(
            "API request failed",
            extra={
                "status_code": response.status_code,
                "exception": exc.__class__.__name__,
            },
        )

    return error_response(
        code=code,
        message=message,
        details=response.data,
        status_code=response.status_code,
    )
