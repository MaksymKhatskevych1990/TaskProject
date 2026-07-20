"""Infrastructure health endpoints."""

import logging

from django.core.cache import caches
from django.db import connections
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class LivenessView(APIView):
    """Report whether the Django process is running."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Return a successful liveness response."""
        return Response({"status": "ok"})


class ReadinessView(APIView):
    """Report whether required data services are available."""

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Check PostgreSQL and Redis connectivity."""
        checks: dict[str, str] = {}
        try:
            connections["default"].ensure_connection()
            checks["database"] = "ok"
        except Exception:
            logger.exception("Database readiness check failed")
            checks["database"] = "error"

        try:
            caches["default"].set("healthcheck", "ok", timeout=5)
            checks["cache"] = (
                "ok" if caches["default"].get("healthcheck") == "ok" else "error"
            )
        except Exception:
            logger.exception("Cache readiness check failed")
            checks["cache"] = "error"

        is_ready = all(value == "ok" for value in checks.values())
        return Response(
            {"status": "ok" if is_ready else "error", "checks": checks},
            status=status.HTTP_200_OK
            if is_ready
            else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
