"""Tests for centralized API exception handling."""

from django.test import SimpleTestCase
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.views import APIView

from apps.common.exceptions import api_exception_handler


class ExceptionHandlerTests(SimpleTestCase):
    """Verify API errors use one predictable envelope."""

    context = {"view": APIView()}

    def test_validation_errors_are_unified(self) -> None:
        """Serializer validation details remain available to clients."""
        response = api_exception_handler(
            ValidationError({"name": ["This field is required."]}),
            self.context,
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertEqual(
            response.data["error"]["details"]["name"],
            ["This field is required."],
        )

    def test_authentication_errors_are_unified(self) -> None:
        """Authentication failures retain their semantic error code."""
        response = api_exception_handler(NotAuthenticated(), self.context)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["error"]["code"], "not_authenticated")
