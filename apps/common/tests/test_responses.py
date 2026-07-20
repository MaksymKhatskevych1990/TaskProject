"""Tests for standard API responses."""

from django.test import SimpleTestCase

from apps.common.responses import error_response, success_response


class ResponseTests(SimpleTestCase):
    """Verify stable success and error envelopes."""

    def test_success_response(self) -> None:
        """Success responses expose data and an optional message."""
        response = success_response(
            {"id": 1},
            message="Created.",
            status_code=201,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "success": True,
                "data": {"id": 1},
                "message": "Created.",
            },
        )

    def test_error_response(self) -> None:
        """Error responses expose a consistent error object."""
        response = error_response(
            code="invalid",
            message="Invalid input.",
            details={"name": ["Required."]},
            status_code=400,
        )

        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["error"]["code"], "invalid")
        self.assertEqual(response.data["error"]["details"]["name"], ["Required."])
